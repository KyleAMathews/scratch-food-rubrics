# frozen_string_literal: true

run_dir = File.expand_path(__dir__)
ledger_path = File.join(run_dir, "05-evidence-ledger.md")
decisions_path = File.join(run_dir, "06-decisions.md")
marker = "## Primary decision — Phase 5 evidence-exhausted universe"

rows = File.readlines(ledger_path, encoding: "UTF-8").map do |line|
  match = line.match(/^\| (R-\d+) (.*?) \| evidence-exhausted-unavailable \| `([^`]+)` \| `([^`]+)` \| .*? \| .*? \| (.*?) \|$/)
  next unless match

  match.captures
end.compact

abort "expected 219 exhausted rows, found #{rows.length}" unless rows.length == 219
abort "duplicate exhausted IDs" unless rows.map(&:first).uniq.length == rows.length

content = File.read(decisions_path, encoding: "UTF-8")
abort "exhausted decision section already present" if content.include?(marker)

lines = []
lines << ""
lines << marker
lines << ""
lines << "Primary decision for every row below: **evidence-exhausted-no-score**. The required evidence sequence was completed, but current identity or score-bearing evidence remains unavailable. No missing field is converted into a zero, disqualification, low-novelty finding, or negative production inference. Each record remains terminal for this run and is excluded from numeric ranking while preserving its individual reason and source."
lines << ""
lines << "| Candidate | Decision | Accepted evidence record | Primary reason |"
lines << "|---|---|---|---|"
rows.each do |candidate_id, name, source, _worker_ref, note|
  lines << "| #{candidate_id} #{name} | evidence-exhausted-no-score | `#{source}` | #{note} |"
end
lines << ""
lines << "Batch result: **219 individually cited evidence-exhausted records decided; 0 numeric scores; 0 inferred failures.**"

File.write(decisions_path, content.rstrip + "\n" + lines.join("\n") + "\n")
