#!/usr/bin/env ruby
# frozen_string_literal: true

require "json"
require "time"

run_dir = File.expand_path(__dir__)
ledger_path = File.join(run_dir, "06-decisions.legacy-v8.10.json")
audit_path = File.join(run_dir, "06-decisions.legacy-v8.10.md")
output_path = File.join(run_dir, "06-decisions.json")

ledger = JSON.parse(File.read(ledger_path, encoding: "UTF-8"))
audit = File.read(audit_path, encoding: "UTF-8")

vectors = {}
audit.each_line do |line|
  next unless (id = line[/\| (R-\d+) /, 1])
  next unless (match = line.match(/`(\d+)\/(\d+)\/(\d+)\/(\d+)\/(\d+) = S\d+`/))

  vectors[id] = match.captures.map(&:to_i)
end

def scaled_complete(vector)
  prep, _retired_volatility, production, coherence, operator = vector
  criteria = {
    "base_prep" => (prep * 25.0 / 20).round,
    "production" => (production * 40.0 / 30).round,
    "coherence" => (coherence * 20.0 / 15).round,
    "operator_format" => (operator * 15.0 / 10).round
  }
  [criteria, criteria.values.sum]
end

def positive_partial?(record)
  reason = record.fetch("reason", "").downcase
  text = record.fetch("rationale", []).join(" ").downcase
  return false if reason.include?("historical") || reason.include?("company marker") || reason.include?("corporate")
  return false if reason.include?("beverage marker") || reason.include?("beverage-first")
  return true if reason.match?(/(?:scratch|production|technique|pastry|dessert|food|roastery|preparation) marker/) && !reason.include?("status conflict")
  return true if reason.match?(/(?:scratch|production|technique|pastry|dessert|food|roastery|preparation).*markers retained/) && !reason.include?("status conflict")

  positive_phrases = [
    /housemade .* (?:is|are) real/,
    /supports .*house-made component/,
    /daily\/in-house guacamole is too narrow/,
    /homemade corned-beef hash is a single scoped item/,
    /homemade soup is a single marker/,
    /homemade-pizza wording is positive/,
    /house-made queso\/marinade are narrow/,
    /homemade naan is positive/,
    /house-made whiz is one marker/
  ]
  positive_phrases.any? { |pattern| text.match?(pattern) }
end

def partial_points(record)
  label = record.fetch("reason", "").downcase
  return 38 if label.include?("exceptional")
  return 34 if label.include?("very strong")
  return 30 if label.include?("strong")
  return 18 if label.include?("technique") || label.include?("preparation")
  return 16 if label.include?("scoped") || label.include?("attributed") || label.include?("source-qualified")
  24
end

stats = Hash.new(0)
ledger["records"].each do |record|
  if record["disposition"] == "scoreable" && vectors.key?(record["id"])
    criteria, total = scaled_complete(vectors.fetch(record["id"]))
    interest = record.dig("score", "i")
    record["score"] = {
      "s" => total,
      "i" => interest,
      "g" => interest ? Math.sqrt(total * interest).round(1) : nil,
      "provenance" => "estimated",
      "state" => "complete",
      "s_earned" => total,
      "s_observed_possible" => 100,
      "s_coverage" => 1.0,
      "confidence" => "medium",
      "criteria" => criteria
    }
    record["reason"] = record["reason"].sub("scoreable", "scoreable-v8.14")
    record["rationale"] << "v8.14 migration: removed legacy volatility from S and proportionally remapped the four retained, previously adjudicated criteria to 25/40/20/15; I was carried unchanged."
    stats["complete_rescored"] += 1
  elsif record["disposition"] == "scoreable"
    earned = record.fetch("reason", "").include?("calibrated anchor") ? 34 : 30
    record["disposition"] = "scratch-eligible-partial"
    record["reason"] = "legacy scalar S cannot be decomposed after turnover removal; current production evidence retained"
    record["score"] = {
      "s" => nil, "i" => nil, "g" => nil, "provenance" => "estimated", "state" => "partial",
      "s_earned" => earned, "s_observed_possible" => 40, "s_coverage" => 0.4,
      "confidence" => "medium",
      "criteria" => { "base_prep" => nil, "production" => earned, "coherence" => nil, "operator_format" => nil }
    }
    record["tier"] = "scratch-eligible partial evidence; legacy scalar requires criterion-level re-review"
    record["ranking_eligible"] = false
    record["rationale"] << "v8.14 migration: the legacy scalar S bundled turnover and has no recoverable criterion vector, so it is not reused; accepted production evidence receives a non-normalized partial score."
    stats["legacy_scalar_to_partial"] += 1
  elsif record["disposition"] == "score-unresolved" && positive_partial?(record)
    earned = partial_points(record)
    record["disposition"] = "scratch-eligible-partial"
    record["reason"] = "credible current production evidence; remaining S criteria unknown"
    record["score"] = {
      "s" => nil,
      "i" => nil,
      "g" => nil,
      "provenance" => "estimated",
      "state" => "partial",
      "s_earned" => earned,
      "s_observed_possible" => 40,
      "s_coverage" => 0.4,
      "confidence" => earned >= 30 ? "medium" : "low",
      "criteria" => {
        "base_prep" => nil,
        "production" => earned,
        "coherence" => nil,
        "operator_format" => nil
      }
    }
    record["tier"] = "scratch-eligible partial evidence; rating state preserved in legacy source"
    record["ranking_eligible"] = false
    record["rationale"] << "v8.14 migration: accepted current production evidence earns a production-criterion partial score; unobserved criteria remain unknown and the partial score is not normalized or ranked."
    stats["partial_rescored"] += 1
  elsif record["disposition"] == "score-unresolved"
    record["disposition"] = "evidence-exhausted-no-score"
    record["reason"] = "no accepted current food-production marker sufficient for scratch eligibility"
    stats["no_score_reclassified"] += 1
  else
    stats["unchanged"] += 1
  end
end

ledger["run_id"] = "2026-07-21-east-millcreek-utah-30-minute-drive-rescore"
ledger["generated_at"] = "2026-07-21T00:00:00-06:00"
ledger["source_artifacts"]["legacy_decisions"] = "06-decisions.legacy-v8.10.json"
ledger["source_artifacts"]["scoring_contract"] = "../restaurant-rubric/phase-6-scoring.md (v8.14)"
File.write(output_path, JSON.pretty_generate(ledger) + "\n")
warn JSON.generate(stats)
