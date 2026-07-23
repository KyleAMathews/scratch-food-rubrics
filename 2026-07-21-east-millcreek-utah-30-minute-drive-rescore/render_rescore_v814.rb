#!/usr/bin/env ruby
# frozen_string_literal: true

require "json"

run_dir = File.expand_path(__dir__)
data = JSON.parse(File.read(File.join(run_dir, "06-decisions.json"), encoding: "UTF-8"))
records = data.fetch("records")
complete = records.select { |record| record.dig("score", "state") == "complete" }
ranked = complete.select { |record| record["ranking_eligible"] }.sort_by { |record| [-record.dig("score", "g"), record["name"]] }
complete_unranked = complete.reject { |record| record["ranking_eligible"] }.sort_by { |record| [-record.dig("score", "s"), record["name"]] }
partial = records.select { |record| record.dig("score", "state") == "partial" }.sort_by { |record| [-record.dig("score", "s_earned"), record["name"]] }
counts = records.group_by { |record| record["disposition"] }.transform_values(&:length)

out = []
out << "# East Millcreek restaurant audit — v8.14 rescore"
out << ""
out << "This is a scoring migration of the frozen 1,650-candidate evidence set. Menu turnover is excluded from `S_scratch` and remains in `I`. Credible current production evidence earns a complete or non-normalized partial scratch score; missing criteria remain unknown."
out << ""
out << "## Migration summary"
out << ""
out << "- Complete new-basis scores: #{complete.length}"
out << "- Complete scores eligible for the G ranking: #{ranked.length}"
out << "- Complete scores kept outside the ranking: #{complete_unranked.length}"
out << "- Scratch-eligible partial scores: #{partial.length}"
out << "- Evidence-exhausted/no-score: #{counts.fetch('evidence-exhausted-no-score', 0)}"
out << "- Positive DQs: #{counts.fetch('positive-DQ', 0)}"
out << "- Familiar standardized U.S. concepts retained under the reversible preference screen: #{counts.fetch('US-standardized-chain-low-novelty', 0)}"
out << ""
out << "Complete rows retain the previously adjudicated base-prep, production, coherence and operator judgments, proportionally remapped to the new 25/40/20/15 maxima. Their old turnover points were discarded. Partial rows are not normalized and receive no `G`."
out << ""
out << "## Complete-score ranking"
out << ""
out << "| Rank | ID | Restaurant | S | I | G |"
out << "|---:|---|---|---:|---:|---:|"
ranked.each_with_index do |record, index|
  score = record.fetch("score")
  out << "| #{index + 1} | #{record['id']} | #{record['name'].gsub('|', '\\|')} | #{score['s']} | #{score['i']} | #{format('%.1f', score['g'])} |"
end
out << ""
out << "## Complete scores outside the ranking"
out << ""
out << "These rows have a complete scratch score but do not meet a separate rating, status, or ranking gate."
out << ""
out << "| ID | Restaurant | S | I | G | Tier |"
out << "|---|---|---:|---:|---:|---|"
complete_unranked.each do |record|
  score = record.fetch("score")
  out << "| #{record['id']} | #{record['name'].gsub('|', '\\|')} | #{score['s']} | #{score['i']} | #{format('%.1f', score['g'])} | #{record['tier'].to_s.gsub('|', '\\|')} |"
end
out << ""
out << "## Scratch-eligible partial-evidence tier"
out << ""
out << "These restaurants have affirmative current scratch evidence but incomplete criterion coverage. `Earned/possible` is deliberately not a percentage score."
out << ""
out << "| ID | Restaurant | Partial S | Coverage | Confidence | Evidence rationale |"
out << "|---|---|---:|---:|---|---|"
partial.each do |record|
  score = record.fetch("score")
  rationale = record.fetch("rationale").first.to_s.gsub('|', '\\|').gsub(/\s+/, ' ')
  out << "| #{record['id']} | #{record['name'].gsub('|', '\\|')} | #{score['s_earned']}/#{score['s_observed_possible']} | #{(score['s_coverage'] * 100).round}% | #{score['confidence']} | #{rationale} |"
end
out << ""
out << "## Interpretation limits"
out << ""
out << "The rescore reuses the frozen accepted evidence and prior primary criterion judgments; it does not refresh ratings, hours or restaurant status after July 2026. The 19 legacy scalar-only calibration rows could not be decomposed without reintroducing turnover, so they correctly appear as partial rather than carrying an invalid complete S."

File.write(File.join(run_dir, "08-results.md"), out.join("\n") + "\n")
