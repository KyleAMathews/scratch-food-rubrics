#!/usr/bin/env ruby
# Deterministic Phase 5 preflight. It maps each successful dispatch row to its
# durable artifact and checks every returned section against the restaurant
# evidence contract. The primary orchestrator reviews its per-record output and
# repairs every flagged record; this script does not accept evidence by itself.

require "json"
require "time"

RUN = File.expand_path(__dir__)
RETURNS = File.join(RUN, "04-worker-returns")
INDEX = File.join(RETURNS, "index.md")
CANDIDATES = File.join(RUN, "02-source-data", "evidence-candidates-after-reviewed-clustering.json")

REQUIRED = [
  "identity", "identity sources", "rating evidence", "price evidence",
  "hours/day-part evidence", "menu quotations", "production/process quotations",
  "seasonality/turnover quotations", "ingredient/sourcing quotations",
  "review-text quotations", "potentially adverse factual quotations",
  "cuisine/format", "neutral factual claims", "search trail", "unavailable fields"
].freeze

def normalize(value)
  value.to_s.unicode_normalize(:nfkd).downcase.gsub(/[^a-z0-9]+/, " ").strip
end

def sections(path)
  text = File.read(path, encoding: "UTF-8")
  file_dates = text.scan(/20\d{2}-\d{2}-\d{2}/).uniq
  level = text.match?(/^##\s+/) ? "##" : "###"
  heads = text.enum_for(:scan, /^#{Regexp.escape(level)}\s+(.+?)\s*$/).map { Regexp.last_match }
  heads.each_with_index.each_with_object([]) do |(match, index), result|
    title = match[1].strip
    next if title.match?(/\A(?:unprocessed|still-unprocessed|batch result|counts|exhaustiveness)/i)
    finish = heads[index + 1]&.begin(0) || text.length
    result << { title: title, text: text[match.begin(0)...finish], file_dates: file_dates }
  end
end

population = JSON.parse(File.read(CANDIDATES, encoding: "UTF-8")).fetch("candidates")
by_id = population.to_h { |candidate| [candidate.fetch("candidate_id"), candidate] }

rows = File.readlines(INDEX, encoding: "UTF-8").each_with_object([]) do |line, result|
  next unless line.start_with?("|")
  next if line.include?("pending") || line.include?("no durable return") || line.match?(/\| dispatched \|\s*$/)
  cells = line.split("|").map(&:strip)
  ids = cells.fetch(3, "").scan(/R-\d{4}/)
  refs = line.scan(/`([^`]+\.md)`/).flatten
  if refs.empty? && !ids.empty?
    batch = cells.fetch(1).to_i
    worker = cells.fetch(4, "")
    inferred = if worker.include?("evidence_batch_001")
      format("batch-%03d-evidence_batch_001.md", batch)
    elsif worker.include?("scratch_dessert_corridor")
      format("batch-%03d-scratch_dessert_corridor.md", batch)
    end
    refs << inferred if inferred && File.file?(File.join(RETURNS, inferred))
  end
  next if ids.empty? || refs.empty?
  result << { batch: cells.fetch(1), ids: ids, refs: refs, worker_ref: cells.fetch(4, "").delete("`") }
end

records = []
mapping_defects = []
repair_overlays = Hash.new { |hash, key| hash[key] = { text: "", file_dates: [] } }
Dir.glob(File.join(RUN, "05-repair-*.md")).sort.each do |path|
  sections(path).each do |section|
    id = section[:title][/R-\d{4}/]
    next unless id
    repair_overlays[id][:text] << "\n" << section[:text]
    repair_overlays[id][:file_dates] |= section[:file_dates]
  end
end

rows.each do |row|
  parsed = row[:refs].flat_map do |ref|
    path = File.join(RETURNS, ref)
    unless File.file?(path)
      mapping_defects << "batch #{row[:batch]} missing file #{ref}"
      next []
    end
    sections(path).map { |section| section.merge(file: ref) }
  end

  unused = parsed.dup
  mapped = {}
  row[:ids].each do |id|
    candidate = by_id[id]
    next unless candidate
    wanted = normalize(candidate["name"])
    hit = unused.find do |section|
      got = normalize(section[:title])
      got == wanted || got.include?(wanted) || wanted.include?(got)
    end
    if hit
      mapped[id] = hit
      unused.delete(hit)
    end
  end

  row[:ids].each do |id|
    next if mapped[id]
    mapped[id] = unused.shift if unused.any?
  end

  if mapped.compact.size != row[:ids].size || unused.any?
    mapping_defects << "batch #{row[:batch]} ids=#{row[:ids].size} sections=#{parsed.size} unmapped=#{row[:ids].reject { |id| mapped[id] }.join(',')} unused=#{unused.map { |s| s[:title] }.join(';')}"
  end

  row[:ids].each do |id|
    candidate = by_id[id]
    section = mapped[id]
    next unless candidate && section
    overlay = repair_overlays[id]
    body = section[:text] + overlay[:text]
    labels = body.scan(/^(?:-\s+)?(?:\*\*)?([^:*\n]+?)(?:\*\*)?:/).flatten.map { |label| normalize(label) }
    urls = body.scan(%r{https?://[^\s)>\]]+})
    aliases = {
      "identity sources" => ["identity and sources", "sources consulted", "identity source", "identity provenance", "sources access"],
      "rating evidence" => ["rating", "ratings", "rating conflict", "literal rating count platform"],
      "price evidence" => ["price", "prices", "price policy", "literal price exhaustion"],
      "hours/day-part evidence" => ["hours", "literal hours status", "historic hours conflict"],
      "menu quotations" => ["menu", "menu evidence", "menu names", "menu mentions", "current raw menu prices", "archived breakfast menu"],
      "production/process quotations" => ["process", "preparation", "production", "bread process"],
      "seasonality/turnover quotations" => ["seasonality", "turnover", "turnover evidence", "turnover availability", "turnover seasonality", "change seasonality", "change cadence", "seasonal dish evidence"],
      "ingredient/sourcing quotations" => ["sourcing", "named ingredients origins", "ingredient sourcing"],
      "review-text quotations" => ["review", "reviews", "product evidence", "service evidence", "defect evidence", "positive product evidence"],
      "potentially adverse factual quotations" => ["potentially adverse factual quotation", "potentially adverse factual and attributed review evidence", "potentially adverse facts", "potentially adverse status facts", "adverse factual review quotations", "reviews adverse facts", "review adverse exhaustion", "adverse", "closure evidence", "status conflict", "defect evidence", "other adverse evidence"],
      "cuisine/format" => ["format", "operator format"],
      "neutral factual claims" => ["neutral factual claims", "accepted URL provenance and neutral factual claims", "neutral boundary", "neutral claim", "neutral claim boundary", "neutral claim boundaries"],
      "search trail" => ["search trail", "exact search trail", "exact required source sequence/search trail", "exact five-stage source sequence/search trail", "exact search trail and unavailable closure", "exact full sequence search trail", "exact search trail unavailable closure", "search unavailable closure", "search record", "searches covered"],
      "unavailable fields" => ["unavailable fields", "unavailable closure", "unavailable closure search sequence", "exact search trail and unavailable closure", "exact search trail unavailable closure", "search unavailable closure", "consolidated unavailable fields closure", "consolidated unavailable closure"]
    }
    missing = REQUIRED.reject do |field|
      terms = ([field] + aliases.fetch(field, [])).map { |term| normalize(term) }
      matched = labels.any? { |label| terms.any? { |term| label == term || label.start_with?(term + " ") } }
      matched ||= field == "identity sources" && body.match?(/identity provenance repair/i) && !urls.empty?
      matched
    end
    dates = (body.scan(/20\d{2}-\d{2}-\d{2}/) + section[:file_dates] + overlay[:file_dates]).uniq
    trail = body[/^(?:-\s+)?(?:\*\*)?(?:Search trail|Exact (?:required|five-stage) source sequence\/search trail|Exact (?:full-sequence )?search trail(?: (?:and|&) unavailable closure|\/unavailable closure)?|Search\/unavailable closure|Search record|Searches covered)(?:\*\*)?:.*$/i] || body[/Search trail included[^\n]*/i]
    unavailable = body[/^(?:-\s+)?(?:\*\*)?(?:Unavailable fields|Unavailable closure(?:\/search sequence)?|Exact search trail(?: (?:and|&) unavailable closure|\/unavailable closure)|Search\/unavailable closure|Consolidated unavailable-fields closure|Consolidated unavailable closure)(?:\*\*)?:.*$/i]
    defects = []
    defects << "missing_fields:#{missing.join(',')}" unless missing.empty?
    defects << "provenance:no_url" if urls.empty?
    defects << "provenance:no_access_date" if dates.empty?
    defects << "search_trail:missing" unless trail
    defects << "unavailable_fields:missing" unless unavailable
    defects << "search_trail:no_query_or_source_detail" if trail && !trail.match?(/quer|search|open|official|review|platform/i)
    defects << "unavailable:bare_none_found" if body.match?(/(?:Unavailable fields|exhausted-unavailable)[^\n]{0,80}\bnone found\b/i)
    defects << "role_boundary:verdict_or_score" if body.match?(/\b(?:DQ\s*[:=]|score\s*[:=]|final confidence\s*[:=]|(?:is|was)\s+(?:eligible|ineligible|disqualified)|qualifies\s+(?:for|as))\b/i)
    records << {
      candidate_id: id,
      candidate_name: candidate["name"],
      returned_title: section[:title],
      worker_file: section[:file],
      worker_ref: row[:worker_ref],
      field_count: labels.uniq.size,
      url_count: urls.uniq.size,
      access_dates: dates.uniq,
      state: defects.empty? ? "preflight-clear" : "repair-review-required",
      defects: defects
    }
  end
end

# A later supplemental/replacement row supersedes an earlier return for the
# same candidate while preserving the earlier artifact in the audit history.
records = records.reverse.uniq { |record| record[:candidate_id] }.reverse

expected = by_id.values.reject { |candidate| candidate["name"].include?("Unnamed OSM") }.map { |candidate| candidate["candidate_id"] }
resolved_unnamed = %w[R-0424 R-1288 R-2156 R-2313 R-2582 R-2686 R-2716 R-2760]
expected |= resolved_unnamed
seen = records.map { |record| record[:candidate_id] }.uniq

output = {
  generated_at: Time.now.iso8601,
  contract: "Phase 5 deterministic preflight; primary-orchestrator semantic review still required",
  expected_count: expected.size,
  record_count: records.size,
  unique_record_count: seen.size,
  missing_candidate_ids: expected - seen,
  unexpected_candidate_ids: seen - expected,
  mapping_defects: mapping_defects,
  clear_count: records.count { |record| record[:state] == "preflight-clear" },
  flagged_count: records.count { |record| record[:state] != "preflight-clear" },
  records: records
}

File.write(File.join(RUN, "05-semantic-preflight.json"), JSON.pretty_generate(output) + "\n")
puts JSON.pretty_generate(output.reject { |key, _| key == :records })
