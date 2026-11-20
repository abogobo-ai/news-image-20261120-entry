// main.ts — news-image-20261120 entry
// Copies entry.png (next to this file) into $MAKEFUN_OUTPUT_DIR/entry.png.
// Node standard library only; no dependencies.
import { copyFileSync, existsSync, mkdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const outDir = process.env.MAKEFUN_OUTPUT_DIR;
if (!outDir) {
  console.error("MAKEFUN_OUTPUT_DIR is not set");
  process.exit(1);
}

const here = dirname(fileURLToPath(import.meta.url));
const src = join(here, "entry.png");
if (!existsSync(src)) {
  console.error("entry.png not found next to main.ts");
  process.exit(1);
}

mkdirSync(outDir, { recursive: true });
const dest = join(outDir, "entry.png");
copyFileSync(src, dest);
// Verify the copy landed byte-identical in size before reporting success.
if (statSync(src).size !== statSync(dest).size) {
  console.error("entry.png copy size mismatch");
  process.exit(1);
}
console.log("entry.png -> " + dest + " (" + statSync(dest).size + " bytes)");
