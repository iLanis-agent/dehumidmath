// Dehumid Math engine - hypothetical arithmetic on labeled norms only.
// Pint ratings, the 2012-to-2019 standard shift and room sizing figures are
// published test-lab norms; real pull depends on temperature, humidity,
// airflow and the unit itself.

const RATIO = 0.72; // labeled norm: 2019-scale pints per 2012-scale pint
const DAMP = ["damp", "very damp", "wet", "extremely wet"];
const BASE = [10, 12, 14, 16]; // labeled norm: pints a day at 500 square feet, 2012 scale
const RATE = [4, 5, 6, 7]; // labeled norm: added pints per further 500 square feet

function tenths(x) { return Math.floor(x * 10 + 0.5) / 10; }
function fixed1(x) { return tenths(x).toFixed(1); }

function roomNeed(sqft, level) {
  if (sqft <= 500) return BASE[level] * sqft / 500;
  return BASE[level] + RATE[level] * (sqft - 500) / 500;
}

function labelTruth(pints, dir) {
  if (!(pints > 0)) throw new Error("the labeled pints must be above zero");
  if (dir === "o2n") return `A ${pints}-pint 2012 label reads about ${fixed1(pints * RATIO)} pints on a 2019 box honestly.`;
  return `A ${pints}-pint 2019 label reads about ${fixed1(pints / RATIO)} pints on a 2012 box honestly.`;
}

function roomTruth(sqft, level, pints, std) {
  if (!(sqft > 0)) throw new Error("the room size must be above zero");
  if (!(pints > 0)) throw new Error("the unit pints must be above zero");
  const need = roomNeed(sqft, level);
  const offer = std === "2012" ? pints : pints / RATIO;
  const dm = tenths(offer - need);
  let verdict;
  if (dm > 0) verdict = `a margin of ${fixed1(dm)} pints honestly`;
  else if (dm < 0) verdict = `${fixed1(-dm)} pints short honestly`;
  else verdict = "exactly matched honestly";
  return `A ${sqft}-square-foot ${DAMP[level]} room asks for ${fixed1(need)} pints a day on the 2012 scale; the ${pints}-pint ${std} unit offers ${fixed1(offer)} pints - ${verdict}.`;
}

function bucketTruth(pull, bucket) {
  if (!(pull > 0)) throw new Error("the daily pull must be above zero");
  if (!(bucket > 0)) throw new Error("the bucket size must be above zero");
  const hours = bucket / pull * 24;
  return `Pulling ${fixed1(pull)} pints a day into a ${bucket}-pint bucket asks for an emptying every ${fixed1(hours)} ${fixed1(hours) === "1.0" ? "hour" : "hours"} honestly.`;
}

if (typeof module !== "undefined") {
  module.exports = { labelTruth, roomTruth, bucketTruth };
}
