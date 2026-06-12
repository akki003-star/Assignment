export default function parseCommaSeparated(str) {
  return str
    .split(",")
    .map((s) => s.trim())
    .filter(Boolean);
}
