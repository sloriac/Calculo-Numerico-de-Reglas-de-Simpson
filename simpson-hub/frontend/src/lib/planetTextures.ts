import * as THREE from "three";

function mulberry32(seed: number) {
  return function () {
    seed |= 0;
    seed = (seed + 0x6d2b79f5) | 0;
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function shadeColor(hex: string, percent: number): string {
  const color = new THREE.Color(hex);
  if (percent >= 0) {
    color.lerp(new THREE.Color("#ffffff"), percent);
  } else {
    color.lerp(new THREE.Color("#000000"), -percent);
  }
  return `#${color.getHexString()}`;
}

const WIDTH = 512;
const HEIGHT = 256;

export function createBandedTexture(baseColor: string, seed: number): THREE.CanvasTexture {
  const canvas = document.createElement("canvas");
  canvas.width = WIDTH;
  canvas.height = HEIGHT;
  const ctx = canvas.getContext("2d")!;
  const rand = mulberry32(seed);

  ctx.fillStyle = baseColor;
  ctx.fillRect(0, 0, WIDTH, HEIGHT);

  const bandCount = 10 + Math.floor(rand() * 5);
  let y = 0;
  while (y < HEIGHT) {
    const bandHeight = 6 + rand() * 22;
    const shade = (rand() - 0.5) * 0.35;
    ctx.fillStyle = shadeColor(baseColor, shade);
    ctx.globalAlpha = 0.55 + rand() * 0.35;
    ctx.fillRect(0, y, WIDTH, bandHeight);
    y += bandHeight;
  }
  ctx.globalAlpha = 1;

  for (let i = 0; i < bandCount * 3; i++) {
    const wy = rand() * HEIGHT;
    ctx.strokeStyle = shadeColor(baseColor, (rand() - 0.5) * 0.4);
    ctx.globalAlpha = 0.2 + rand() * 0.3;
    ctx.lineWidth = 1 + rand() * 2;
    ctx.beginPath();
    ctx.moveTo(0, wy);
    for (let x = 0; x <= WIDTH; x += 16) {
      ctx.lineTo(x, wy + Math.sin(x * 0.02 + rand() * 10) * 4);
    }
    ctx.stroke();
  }
  ctx.globalAlpha = 1;

  const stormX = WIDTH * (0.2 + rand() * 0.6);
  const stormY = HEIGHT * (0.3 + rand() * 0.4);
  const stormRadius = 18 + rand() * 14;
  const gradient = ctx.createRadialGradient(stormX, stormY, 0, stormX, stormY, stormRadius);
  gradient.addColorStop(0, shadeColor(baseColor, 0.25));
  gradient.addColorStop(0.6, shadeColor(baseColor, -0.15));
  gradient.addColorStop(1, "rgba(0,0,0,0)");
  ctx.fillStyle = gradient;
  ctx.beginPath();
  ctx.ellipse(stormX, stormY, stormRadius, stormRadius * 0.65, 0, 0, Math.PI * 2);
  ctx.fill();

  const texture = new THREE.CanvasTexture(canvas);
  texture.wrapS = THREE.RepeatWrapping;
  texture.colorSpace = THREE.SRGBColorSpace;
  return texture;
}

export function createMottledTexture(baseColor: string, seed: number): THREE.CanvasTexture {
  const canvas = document.createElement("canvas");
  canvas.width = WIDTH;
  canvas.height = HEIGHT;
  const ctx = canvas.getContext("2d")!;
  const rand = mulberry32(seed);

  ctx.fillStyle = baseColor;
  ctx.fillRect(0, 0, WIDTH, HEIGHT);

  for (let i = 0; i < 90; i++) {
    const x = rand() * WIDTH;
    const y = rand() * HEIGHT;
    const radius = 10 + rand() * 34;
    const shade = (rand() - 0.55) * 0.5;
    ctx.fillStyle = shadeColor(baseColor, shade);
    ctx.globalAlpha = 0.35 + rand() * 0.3;
    ctx.beginPath();
    ctx.ellipse(x, y, radius, radius * (0.5 + rand() * 0.5), rand() * Math.PI, 0, Math.PI * 2);
    ctx.fill();
  }
  ctx.globalAlpha = 1;

  const imageData = ctx.getImageData(0, 0, WIDTH, HEIGHT);
  for (let i = 0; i < imageData.data.length; i += 4) {
    const noise = (rand() - 0.5) * 14;
    imageData.data[i] = Math.min(255, Math.max(0, imageData.data[i] + noise));
    imageData.data[i + 1] = Math.min(255, Math.max(0, imageData.data[i + 1] + noise));
    imageData.data[i + 2] = Math.min(255, Math.max(0, imageData.data[i + 2] + noise));
  }
  ctx.putImageData(imageData, 0, 0);

  const texture = new THREE.CanvasTexture(canvas);
  texture.wrapS = THREE.RepeatWrapping;
  texture.colorSpace = THREE.SRGBColorSpace;
  return texture;
}
