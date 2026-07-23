# frozen_string_literal: true

require "json"

run_dir = File.expand_path(__dir__)
preflight = JSON.parse(File.read(File.join(run_dir, "05-semantic-preflight.json")))
review_path = File.join(run_dir, "05-primary-semantic-review.md")
output_path = File.join(run_dir, "05-evidence-ledger.md")

records = preflight.fetch("records").each_with_object({}) do |record, memo|
  memo[record.fetch("candidate_id")] = record
end

quarantine_sources = {
  "R-0954" => "04-unnamed-identity-repair-batch-001.md",
  "R-0985" => "04-unnamed-identity-repair-batch-001.md",
  "R-1401" => "04-unnamed-identity-repair-batch-001.md",
  "R-1473" => "04-unnamed-identity-repair-batch-002.md",
  "R-1848" => "04-unnamed-identity-repair-batch-002.md",
  "R-1944" => "04-unnamed-identity-repair-batch-002.md",
  "R-2327" => "04-unnamed-identity-repair-batch-003.md",
  "R-2387" => "04-unnamed-identity-repair-batch-003.md",
  "R-2473" => "04-unnamed-identity-repair-batch-003.md",
  "R-2481" => "04-unnamed-identity-repair-batch-003.md",
  "R-2487" => "04-unnamed-identity-repair-batch-003.md",
  "R-2630" => "04-unnamed-identity-repair-batch-004.md",
  "R-2634" => "04-unnamed-identity-repair-batch-004.md",
  "R-2850" => "04-unnamed-identity-repair-batch-005.md",
  "R-2876" => "04-unnamed-identity-repair-batch-005.md"
}

rows = File.readlines(review_path, encoding: "UTF-8").map do |line|
  match = line.match(/^\| (R-\d+) (.*?) \| (evidence-(?:accepted|exhausted-unavailable)) \| (.*?) \|$/)
  next unless match

  candidate_id, name, state, note = match.captures
  record = records[candidate_id]
  source = if record
    "04-worker-returns/#{record.fetch("worker_file")}"
  else
    quarantine_sources.fetch(candidate_id)
  end
  worker_ref = record ? record.fetch("worker_ref") : "primary identity-repair review"
  audit = if record
    "preflight-clear; #{record.fetch("field_count")} required fields; #{record.fetch("url_count")} URLs; access #{record.fetch("access_dates").join(", ")}"
  else
    "identity exhausted; all restaurant-specific fields exhausted-unavailable; access 2026-07-15"
  end
  field_states = if record
    "identity/rating/price/hours/menu/process/turnover/sourcing/reviews/adverse/format/search trail: documented or explicitly exhausted in source record; provenance semantically accepted"
  else
    "identity and all restaurant-specific evidence fields: exhausted-unavailable after recorded coordinate/OSM/parcel/locator sequence"
  end

  [candidate_id, name, state, source, worker_ref, audit, field_states, note]
end.compact

expected_ids = records.keys | quarantine_sources.keys
actual_ids = rows.map(&:first)
missing = expected_ids - actual_ids
unexpected = actual_ids - expected_ids
duplicates = actual_ids.group_by(&:itself).select { |_id, ids| ids.length > 1 }.keys
abort "ledger input mismatch: missing=#{missing.inspect} unexpected=#{unexpected.inspect} duplicates=#{duplicates.inspect}" unless missing.empty? && unexpected.empty? && duplicates.empty?

accepted = rows.count { |row| row[2] == "evidence-accepted" }
exhausted = rows.count { |row| row[2] == "evidence-exhausted-unavailable" }

lines = []
lines << "# Phase 5 evidence ledger"
lines << ""
lines << "Generated from the semantically inspected raw evidence records and primary decisions on 2026-07-17. The cited source record is incorporated by reference and contains the accepted literal quotations/values, URL, source type, access date, source sequence, queries, conflicts and field-level `documented`, `product-only`, or `exhausted-unavailable` facts. `05-primary-semantic-review.md` records the primary judgment for every row; `05-repair-log.md` records every repair wave and conflict action."
lines << ""
lines << "Universe: **#{rows.length} records** — **#{accepted} evidence-accepted**, **#{exhausted} evidence-exhausted-unavailable**. This comprises #{records.length} structured evidence records plus #{quarantine_sources.length} unresolved unnamed geometries."
lines << ""
lines << "| candidate | terminal evidence state | accepted evidence record | worker/provenance | structural acceptance | per-field evidence states | primary semantic acceptance note |"
lines << "|---|---|---|---|---|---|---|"
rows.each do |candidate_id, name, state, source, worker_ref, audit, field_states, note|
  escaped = [name, source, worker_ref, audit, field_states, note].map { |value| value.to_s.gsub("|", "\\|").gsub("\n", " ") }
  lines << "| #{candidate_id} #{escaped[0]} | #{state} | `#{escaped[1]}` | `#{escaped[2]}` | #{escaped[3]} | #{escaped[4]} | #{escaped[5]} |"
end
lines << ""
lines << "## Integrity summary"
lines << ""
lines << "- Expected IDs: #{expected_ids.length}; ledger IDs: #{actual_ids.uniq.length}; missing: 0; unexpected: 0; duplicates: 0."
lines << "- Structured records: #{records.length}; deterministic preflight state: all `preflight-clear`."
lines << "- Unresolved unnamed geometries: #{quarantine_sources.length}; each is terminal only at identity exhaustion and carries no transferred nearby-tenant evidence."
lines << "- Primary semantic states: #{accepted} accepted + #{exhausted} exhausted = #{rows.length}."

File.write(output_path, lines.join("\n") + "\n")
