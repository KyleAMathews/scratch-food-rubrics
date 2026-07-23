#!/usr/bin/env ruby
# frozen_string_literal: true

require "digest"
require "json"

path = File.join(__dir__, "06-decisions.json")
data = JSON.parse(File.read(path, encoding: "UTF-8"))
records = data.fetch("records")
errors = []

errors << "population #{records.length} != 1650" unless records.length == 1650
ids = records.map { |record| record.fetch("id") }
errors << "duplicate ids: #{ids.tally.select { |_id, count| count > 1 }.keys.join(', ')}" unless ids.uniq.length == ids.length

records.each do |record|
  score = record["score"]
  next unless score

  if score["state"] == "partial"
    errors << "#{record['id']}: partial s/i/g must be null" unless %w[s i g].all? { |key| score[key].nil? }
    required = %w[s_earned s_observed_possible s_coverage confidence criteria]
    errors << "#{record['id']}: incomplete partial metadata" unless required.all? { |key| score.key?(key) }
    errors << "#{record['id']}: normalized partial" unless (score["s_coverage"] - score["s_observed_possible"] / 100.0).abs < 0.0001
    observed = score.fetch("criteria").values.compact.sum
    errors << "#{record['id']}: partial sum mismatch" unless observed == score["s_earned"]
    errors << "#{record['id']}: partial marked ranking eligible" if record["ranking_eligible"]
  elsif score["state"] == "complete"
    criteria = score.fetch("criteria")
    maxima = { "base_prep" => 25, "production" => 40, "coherence" => 20, "operator_format" => 15 }
    maxima.each do |key, maximum|
      value = criteria[key]
      errors << "#{record['id']}: #{key}=#{value.inspect}" unless value.is_a?(Numeric) && value.between?(0, maximum)
    end
    errors << "#{record['id']}: complete sum mismatch" unless criteria.values.sum == score["s"]
    expected_g = Math.sqrt(score["s"] * score["i"]).round(1)
    errors << "#{record['id']}: G #{score['g']} != #{expected_g}" unless score["g"] == expected_g
  else
    errors << "#{record['id']}: score state missing"
  end
end

counts = records.group_by { |record| record.fetch("disposition") }.transform_values(&:length).sort.to_h
report = {
  "schema_contract" => "restaurant v8.14 migration invariants",
  "population" => records.length,
  "unique_ids" => ids.uniq.length,
  "disposition_counts" => counts,
  "errors" => errors,
  "passed" => errors.empty?,
  "sha256" => Digest::SHA256.file(path).hexdigest
}
File.write(File.join(__dir__, "06-rescore-validation.json"), JSON.pretty_generate(report) + "\n")
puts JSON.pretty_generate(report)
exit(errors.empty? ? 0 : 1)
