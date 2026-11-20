/**
 * Entry program for make.fun "news-image-20261120".
 *
 * The repository ships a finished news image, entry.png, drawn by the
 * Python scripts in tools/. This program's job is narrow: prove the
 * bundled file is a well-formed PNG inside the competition limits —
 * signature, IHDR dimensions, the 1 MiB cap, and a full chunk walk
 * that re-checks every chunk's CRC and ends exactly at IEND — then
 * publish its bytes, untouched, as /output/entry.png and report a
 * one-line JSON manifest (including the SHA-256 of what was written).
 *
 * Node standard library only; no network access is needed or used.
 */
import { createHash } from "node:crypto";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const MAX_BYTES = 1_048_576; // 1 MiB, the competition's size cap
const MAX_SIDE = 1_024; // neither dimension may exceed 1024 px
const PNG_SIGNATURE: readonly number[] = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];

function reject(reason: string): never {
  throw new Error(`entry.png is not acceptable: ${reason}`);
}

/** Read the two big-endian uint32 fields of the IHDR chunk. */
function headerDimensions(png: Buffer): { width: number; height: number } {
  // Layout: 8-byte signature, then IHDR = length(4) + "IHDR"(4) + data.
  // Width and height are the first two uint32s of the IHDR data.
  if (png.length < 8 + 8 + 8) reject("file too short to hold a PNG header");
  for (let i = 0; i < PNG_SIGNATURE.length; i++) {
    if (png[i] !== PNG_SIGNATURE[i]) reject("missing PNG signature");
  }
  const ihdrType = png.toString("ascii", 12, 16);
  if (ihdrType !== "IHDR") reject(`first chunk is ${ihdrType}, expected IHDR`);
  return { width: png.readUInt32BE(16), height: png.readUInt32BE(20) };
}

// PNG chunk checksums are CRC-32 (ISO 3309), computed over type+data.
const CRC_TABLE = ((): Uint32Array => {
  const table = new Uint32Array(256);
  for (let n = 0; n < 256; n++) {
    let c = n;
    for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1;
    table[n] = c >>> 0;
  }
  return table;
})();

function crc32(buf: Buffer, from: number, to: number): number {
  let c = 0xffffffff;
  for (let i = from; i < to; i++) c = CRC_TABLE[(c ^ buf[i]) & 0xff] ^ (c >>> 8);
  return (c ^ 0xffffffff) >>> 0;
}

/**
 * Walk the whole chunk stream. Every chunk is length(4) + type(4) +
 * data(length) + CRC(4); each stored CRC must match the recomputed
 * one, and the walk must land exactly on the end of the file just
 * after an IEND chunk, so a truncated, padded or corrupted file fails.
 * Returns the number of chunks seen.
 */
function walkChunks(png: Buffer): number {
  let offset = 8; // skip the signature
  let count = 0;
  for (;;) {
    if (offset + 8 > png.length) reject("chunk stream ends mid-header");
    const length = png.readUInt32BE(offset);
    const type = png.toString("ascii", offset + 4, offset + 8);
    const next = offset + 8 + length + 4;
    if (next > png.length) reject(`chunk ${type} overruns the file`);
    const stored = png.readUInt32BE(next - 4);
    if (crc32(png, offset + 4, next - 4) !== stored) {
      reject(`chunk ${type} fails its CRC check`);
    }
    count += 1;
    offset = next;
    if (type === "IEND") break;
  }
  if (offset !== png.length) reject("trailing bytes after IEND");
  return count;
}

function main(): void {
  const repoDir = dirname(fileURLToPath(import.meta.url));
  const source = readFileSync(join(repoDir, "entry.png"));

  if (source.length > MAX_BYTES) {
    reject(`${source.length} bytes exceeds the ${MAX_BYTES}-byte cap`);
  }
  const { width, height } = headerDimensions(source);
  if (width > MAX_SIDE || height > MAX_SIDE) {
    reject(`dimensions ${width}x${height} exceed ${MAX_SIDE}x${MAX_SIDE}`);
  }
  const chunks = walkChunks(source);

  const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
  mkdirSync(outDir, { recursive: true });
  const target = join(outDir, "entry.png");
  writeFileSync(target, source);

  const written = readFileSync(target);
  if (!written.equals(source)) reject("the written copy differs from entry.png");
  const digest = createHash("sha256").update(written).digest("hex");
  console.log(
    JSON.stringify({
      artifact: "entry.png",
      bytes: written.length,
      width,
      height,
      chunks,
      verified: true,
      sha256: digest,
    }),
  );
}

main();
