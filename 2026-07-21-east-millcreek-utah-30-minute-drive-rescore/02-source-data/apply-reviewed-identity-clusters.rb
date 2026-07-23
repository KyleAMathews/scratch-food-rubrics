#!/usr/bin/env ruby
# frozen_string_literal: true

require "json"

abort "usage: apply-reviewed-identity-clusters.rb INPUT.json OUTPUT.json REVIEW.json" unless ARGV.length == 3

input_path, output_path, review_path = ARGV
document = JSON.parse(File.read(input_path))
candidates = document.fetch("candidates")
by_id = candidates.to_h { |row| [row.fetch("candidate_id"), row] }
origin = [40.7067859, -111.8192536]

same_venue_keep = {
  %w[R-2062 R-2071].sort => "R-2071",
  %w[R-0614 R-1570].sort => "R-0614",
  %w[R-0709 R-1521].sort => "R-1521",
  %w[R-1471 R-2910].sort => "R-1471",
  %w[R-1318 R-1680].sort => "R-1680", # verified relocation to South Salt Lake
  %w[R-2084 R-2889].sort => "R-2084",
  %w[R-2365 R-2921].sort => "R-2365",
  %w[R-0022 R-2232].sort => "R-0022"
}

same_concept_pairs = [
  %w[R-0029 R-0836], %w[R-0045 R-2194], %w[R-0131 R-2357],
  %w[R-0162 R-0168], %w[R-0208 R-2175], %w[R-0217 R-2426],
  %w[R-0289 R-0819], %w[R-0338 R-0988], %w[R-0475 R-2403],
  %w[R-0702 R-2566], %w[R-0791 R-1253], %w[R-0941 R-2001],
  %w[R-0942 R-1661], %w[R-1024 R-1062], %w[R-1038 R-1149],
  %w[R-1137 R-1584], %w[R-1169 R-1756], %w[R-1262 R-2420],
  %w[R-1268 R-2435], %w[R-1354 R-1583], %w[R-1364 R-2057],
  %w[R-1381 R-1956], %w[R-1661 R-1941], %w[R-1759 R-2107],
  %w[R-2154 R-2515], %w[R-2183 R-2324], %w[R-2388 R-2545],
  %w[R-2482 R-2053]
]

different_pairs = [
  %w[R-0018 R-1453], %w[R-0210 R-2248], %w[R-0253 R-0748],
  %w[R-0814 R-0863], %w[R-1063 R-2173], %w[R-1063 R-2676],
  %w[R-1516 R-2320], %w[R-1642 R-2289], %w[R-2083 R-2191],
  %w[R-2173 R-2676], %w[R-0057 R-0058], %w[R-0110 R-0652],
  %w[R-0662 R-2462], %w[R-1771 R-1979]
]

unresolved_pairs = [
  %w[R-1473 R-2686], %w[R-1848 R-2716], %w[R-2481 R-2582]
]

def distance(origin, row)
  point = row["point"]
  return Float::INFINITY unless point && point["lat"] && point["lon"]

  lat1, lon1 = origin.map { |x| x * Math::PI / 180 }
  lat2 = point["lat"].to_f * Math::PI / 180
  lon2 = point["lon"].to_f * Math::PI / 180
  dlat = lat2 - lat1
  dlon = lon2 - lon1
  a = Math.sin(dlat / 2)**2 + Math.cos(lat1) * Math.cos(lat2) * Math.sin(dlon / 2)**2
  6_371_000 * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a))
end

# Union same-concept pairs so overlapping pairs (for example Roxberry) choose one representative.
parent = {}
find = lambda do |id|
  parent[id] ||= id
  parent[id] = find.call(parent[id]) unless parent[id] == id
  parent[id]
end
same_concept_pairs.each do |left, right|
  a = find.call(left)
  b = find.call(right)
  parent[b] = a unless a == b
end

groups = parent.keys.group_by { |id| find.call(id) }.values
removed = {}
decisions = []

same_venue_keep.each do |pair, keep|
  drop = (pair - [keep]).fetch(0)
  removed[drop] = { "reason" => "reviewed-same-venue", "representative_id" => keep }
  decisions << { "ids" => pair, "decision" => "same-venue", "keep" => keep, "remove" => [drop] }
end

groups.each do |ids|
  keep = ids.min_by { |id| [distance(origin, by_id.fetch(id)), id] }
  drops = ids - [keep]
  drops.each do |drop|
    removed[drop] = { "reason" => "reviewed-same-concept-farther-branch", "representative_id" => keep }
  end
  decisions << { "ids" => ids.sort, "decision" => "same-concept-branches", "keep" => keep, "remove" => drops.sort }
end

different_pairs.each { |ids| decisions << { "ids" => ids.sort, "decision" => "different" } }
unresolved_pairs.each { |ids| decisions << { "ids" => ids.sort, "decision" => "unresolved" } }

output_candidates = candidates.reject { |row| removed.key?(row.fetch("candidate_id")) }
review = {
  "reviewed_at" => "2026-07-15",
  "reviewed_pair_count" => same_venue_keep.length + same_concept_pairs.length + different_pairs.length + unresolved_pairs.length,
  "decision_cluster_count" => decisions.length,
  "cluster_counts" => decisions.group_by { |row| row["decision"] }.transform_values(&:length),
  "removed_count" => removed.length,
  "remaining_count" => output_candidates.length,
  "decisions" => decisions.sort_by { |row| row["ids"] }
}

output = document.merge(
  "generated_at" => "2026-07-15",
  "rules" => Array(document["rules"]) + ["reviewed-fuzzy-identity-clustering-v1"],
  "counts" => document.fetch("counts", {}).merge(
    "before_reviewed_fuzzy_clustering" => candidates.length,
    "removed_by_reviewed_fuzzy_clustering" => removed.length,
    "after_reviewed_fuzzy_clustering" => output_candidates.length
  ),
  "candidates" => output_candidates
)

File.write(output_path, JSON.pretty_generate(output) + "\n")
File.write(review_path, JSON.pretty_generate(review) + "\n")
