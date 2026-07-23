#!/usr/bin/env ruby
# frozen_string_literal: true

require "json"
require "set"
require "uri"

abort "usage: propose-identity-clusters.rb INPUT.json" unless ARGV.length == 1

document = JSON.parse(File.read(ARGV.fetch(0)))
candidates = document.is_a?(Hash) ? document.fetch("candidates") : document

def text(value)
  value.to_s.unicode_normalize(:nfkd)
       .encode("ASCII", invalid: :replace, undef: :replace, replace: "")
       .downcase.gsub("&", " and ").gsub(/[^a-z0-9]+/, " ").strip
end

LEGAL_WORDS = Set.new(%w[the restaurant restaurants cafe cafes grill kitchen pub bar company co llc inc]).freeze

def name_tokens(candidate)
  names = [candidate["name"], *Array(candidate["aliases"])]
  names.flat_map { |name| text(name).split }.reject { |token| LEGAL_WORDS.include?(token) }.uniq.sort
end

def phone(candidate)
  digits = candidate["phone"].to_s.gsub(/\D/, "")
  digits = digits[-10, 10] if digits.length > 10
  digits.length == 10 ? digits : nil
end

def domain(candidate)
  raw = candidate["domain"].to_s.strip
  return nil if raw.empty?

  host = URI.parse(raw.include?("://") ? raw : "https://#{raw}").host.to_s.downcase
  host = host.sub(/\Awww\./, "")
  host.empty? ? nil : host
rescue URI::InvalidURIError
  nil
end

def point(candidate)
  value = candidate["point"]
  return nil unless value.is_a?(Hash) && value["lat"] && value["lon"]

  [value["lat"].to_f, value["lon"].to_f]
end

def distance_m(left, right)
  return nil unless left && right

  lat1, lon1 = left.map { |x| x * Math::PI / 180 }
  lat2, lon2 = right.map { |x| x * Math::PI / 180 }
  dlat = lat2 - lat1
  dlon = lon2 - lon1
  a = Math.sin(dlat / 2)**2 + Math.cos(lat1) * Math.cos(lat2) * Math.sin(dlon / 2)**2
  6_371_000 * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a))
end

def dice(left, right)
  a = left.to_set
  b = right.to_set
  return 0.0 if a.empty? || b.empty?

  2.0 * (a & b).length / (a.length + b.length)
end

rows = candidates.map do |candidate|
  {
    "candidate" => candidate,
    "id" => candidate.fetch("candidate_id"),
    "tokens" => name_tokens(candidate),
    "token_key" => name_tokens(candidate).join(" "),
    "phone" => phone(candidate),
    "domain" => domain(candidate),
    "point" => point(candidate),
    "address" => text(candidate["address"])
  }
end

# Blocking keeps comparisons cheap. Each block represents a plausible shared identity signal.
blocks = Hash.new { |hash, key| hash[key] = [] }
rows.each do |row|
  blocks[["tokens", row["token_key"]]] << row unless row["token_key"].empty?
  blocks[["phone", row["phone"]]] << row if row["phone"]
  blocks[["domain", row["domain"]]] << row if row["domain"]
  blocks[["address", row["address"]]] << row unless row["address"].empty?
  row["tokens"].each { |token| blocks[["rare-token", token]] << row if token.length >= 6 }
end

pairs = {}
blocks.each_value do |members|
  next if members.length < 2 || members.length > 80

  members.combination(2) do |left, right|
    key = [left["id"], right["id"]].sort
    pairs[key] ||= [left, right]
  end
end

proposals = pairs.values.map do |left, right|
  reasons = []
  meters = distance_m(left["point"], right["point"])
  similarity = dice(left["tokens"], right["tokens"])
  reasons << "same-phone" if left["phone"] && left["phone"] == right["phone"]
  reasons << "same-domain" if left["domain"] && left["domain"] == right["domain"]
  reasons << "same-address" if !left["address"].empty? && left["address"] == right["address"]
  reasons << "same-name-token-set" if !left["token_key"].empty? && left["token_key"] == right["token_key"]
  reasons << "near-100m" if meters && meters <= 100
  reasons << "near-name-match" if meters && meters <= 500 && similarity >= 0.66

  # Shared domains and phone numbers are often corporate/hotel infrastructure,
  # not shared restaurant identities. Require name agreement unless the names
  # independently match or a similar name occupies the same physical site.
  supported = reasons.include?("same-name-token-set") ||
              reasons.include?("near-name-match") ||
              (reasons.include?("same-address") && similarity >= 0.4) ||
              (reasons.include?("same-phone") && similarity >= 0.5) ||
              (reasons.include?("same-domain") && similarity >= 0.66)
  next unless supported

  confidence = if (reasons & %w[same-phone same-address]).any? && similarity >= 0.66
                 "high"
               elsif reasons.include?("same-name-token-set") ||
                     (reasons.include?("same-domain") && similarity >= 0.66)
                 "medium"
               else
                 "review"
               end

  {
    "left_id" => left["id"],
    "left_name" => left["candidate"]["name"],
    "left_address" => left["candidate"]["address"],
    "right_id" => right["id"],
    "right_name" => right["candidate"]["name"],
    "right_address" => right["candidate"]["address"],
    "confidence" => confidence,
    "reasons" => reasons,
    "name_token_dice" => similarity.round(3),
    "distance_m" => meters&.round(1),
    "review_decision" => nil,
    "review_note" => nil
  }
end.compact

order = { "high" => 0, "medium" => 1, "review" => 2 }
proposals.sort_by! { |row| [order.fetch(row["confidence"]), row["left_id"], row["right_id"]] }

puts JSON.pretty_generate(
  "algorithm_version" => 1,
  "input_count" => candidates.length,
  "proposal_count" => proposals.length,
  "decision_contract" => {
    "same-venue" => "merge duplicate identity",
    "same-concept-branches" => "share concept evidence; retain nearest branch unless locally different",
    "different" => "do not merge",
    "unresolved" => "identity repair before evidence research"
  },
  "proposals" => proposals
)
