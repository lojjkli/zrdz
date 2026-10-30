import * as THREE from 'three';

const cache = new Map<string, THREE.Texture>();

export const canvasTex = (
	key: string,
	w: number,
	h: number,
	draw: (ctx: CanvasRenderingContext2D) => void,
	opts: {repeat?: [number, number]; nearest?: boolean} = {},
) => {
	const hit = cache.get(key);
	if (hit) return hit;
	const c = document.createElement('canvas');
	c.width = w;
	c.height = h;
	const ctx = c.getContext('2d')!;
	draw(ctx);
	const t = new THREE.CanvasTexture(c);
	t.colorSpace = THREE.SRGBColorSpace;
	t.anisotropy = 8;
	if (opts.repeat) {
		t.wrapS = t.wrapT = THREE.RepeatWrapping;
		t.repeat.set(...opts.repeat);
	}
	if (opts.nearest) {
		t.magFilter = THREE.NearestFilter;
	}
	cache.set(key, t);
	return t;
};

// deterministic pseudo random
export const rand = (seed: number) => {
	const x = Math.sin(seed * 127.1 + 311.7) * 43758.5453;
	return x - Math.floor(x);
};

export type FaceKind =
	| 'smile' | 'worried' | 'sad' | 'kli' | 'grin' | 'scream' | 'happy'
	| 'lia' | 'liasad' | 'liacry' | 'liashock' | 'hearts' | 'angry' | 'duck' | 'duckwink' | 'shock' | 'sick' | 'kliwide' | 'blank' | 'klisad' | 'klishock';

export const faceTexture = (kind: FaceKind) =>
	canvasTex('face-' + kind, 256, 256, (ctx) => {
		ctx.clearRect(0, 0, 256, 256);
		if (kind === 'blank') return;
		if (drawExtraFace(ctx, kind)) return;
		if (kind === 'klisad' || kind === 'klishock') {
			ctx.fillStyle = '#ffffff';
			const px = 256 / 8;
			const on: [number, number][] =
				kind === 'klisad' ? [[2, 5], [3, 5], [4, 5], [5, 5], [1, 6], [6, 6]] : [[3, 4], [4, 4], [2, 5], [5, 5], [3, 6], [4, 6]];
			for (const [x, y] of on) ctx.fillRect(x * px, y * px - px * 1.2, px, px);
			return;
		}
		if (kind === 'kli') {
			// lojjkli's pixel smile, straight from the skin (8x8 face, rows 5-6)
			ctx.fillStyle = '#ffffff';
			const px = 256 / 8;
			const on: [number, number][] = [
				[1, 5], [6, 5], [2, 6], [3, 6], [4, 6], [5, 6],
			];
			for (const [x, y] of on) ctx.fillRect(x * px, y * px - px * 1.2, px, px);
			return;
		}
		ctx.fillStyle = '#111';
		ctx.strokeStyle = '#111';
		ctx.lineCap = 'round';
		// eyes
		const eye = (x: number, y: number, ry: number) => {
			ctx.beginPath();
			ctx.ellipse(x, y, 12, ry, 0, 0, Math.PI * 2);
			ctx.fill();
		};
		if (kind === 'happy') {
			ctx.lineWidth = 11;
			for (const x of [92, 164]) {
				ctx.beginPath();
				ctx.arc(x, 112, 16, Math.PI * 1.1, Math.PI * 1.9);
				ctx.stroke();
			}
		} else if (kind === 'scream') {
			eye(92, 100, 20);
			eye(164, 100, 20);
		} else if (kind === 'worried' || kind === 'sad') {
			eye(92, 108, 16);
			eye(164, 108, 16);
			ctx.lineWidth = 8;
			ctx.beginPath();
			ctx.moveTo(70, 78);
			ctx.lineTo(108, 70);
			ctx.moveTo(186, 78);
			ctx.lineTo(148, 70);
			ctx.stroke();
		} else {
			eye(92, 104, 18);
			eye(164, 104, 18);
		}
		ctx.lineWidth = 10;
		ctx.beginPath();
		if (kind === 'smile' || kind === 'happy') {
			ctx.arc(128, 128, 52, Math.PI * 0.2, Math.PI * 0.8);
			ctx.stroke();
		} else if (kind === 'grin') {
			ctx.fillStyle = '#111';
			ctx.arc(128, 140, 46, 0, Math.PI);
			ctx.fill();
			ctx.fillStyle = '#fff';
			ctx.fillRect(92, 140, 72, 12);
		} else if (kind === 'sad') {
			ctx.arc(128, 200, 40, Math.PI * 1.2, Math.PI * 1.8);
			ctx.stroke();
		} else if (kind === 'worried') {
			ctx.moveTo(96, 178);
			ctx.quadraticCurveTo(128, 160, 160, 178);
			ctx.stroke();
		} else if (kind === 'scream') {
			ctx.ellipse(128, 176, 26, 36, 0, 0, Math.PI * 2);
			ctx.fill();
		}
	});

const heartPath = (ctx: CanvasRenderingContext2D, cx: number, cy: number, s: number) => {
	ctx.beginPath();
	ctx.moveTo(cx, cy + s * 0.9);
	ctx.bezierCurveTo(cx - s * 1.5, cy - s * 0.1, cx - s * 0.7, cy - s * 1.3, cx, cy - s * 0.45);
	ctx.bezierCurveTo(cx + s * 0.7, cy - s * 1.3, cx + s * 1.5, cy - s * 0.1, cx, cy + s * 0.9);
	ctx.fill();
};

// Faces added for the Lia story. Returns true when it handled the kind.
const drawExtraFace = (ctx: CanvasRenderingContext2D, kind: FaceKind) => {
	const ink = '#1b1320';
	ctx.lineCap = 'round';
	ctx.lineJoin = 'round';
	const blush = (a = 0.55) => {
		ctx.fillStyle = `rgba(255,110,150,${a})`;
		for (const x of [70, 186]) {
			ctx.beginPath();
			ctx.ellipse(x, 152, 20, 11, 0, 0, Math.PI * 2);
			ctx.fill();
		}
	};
	const liaEye = (x: number, y: number, open = 1) => {
		ctx.fillStyle = ink;
		ctx.beginPath();
		ctx.ellipse(x, y, 15, 21 * open, 0, 0, Math.PI * 2);
		ctx.fill();
		if (open > 0.5) {
			ctx.fillStyle = '#fff';
			ctx.beginPath();
			ctx.arc(x + 5, y - 8, 6, 0, Math.PI * 2);
			ctx.fill();
			ctx.beginPath();
			ctx.arc(x - 4, y + 7, 3, 0, Math.PI * 2);
			ctx.fill();
		}
		// lashes
		ctx.strokeStyle = ink;
		ctx.lineWidth = 6;
		const side = x < 128 ? -1 : 1;
		ctx.beginPath();
		ctx.moveTo(x + side * 12, y - 16 * open);
		ctx.lineTo(x + side * 24, y - 26 * open - 2);
		ctx.stroke();
	};
	switch (kind) {
		case 'lia':
		case 'liashock':
		case 'liasad': {
			blush();
			liaEye(92, 108);
			liaEye(164, 108);
			ctx.strokeStyle = ink;
			ctx.fillStyle = ink;
			ctx.lineWidth = 8;
			ctx.beginPath();
			if (kind === 'lia') {
				ctx.arc(128, 150, 24, Math.PI * 0.15, Math.PI * 0.85);
				ctx.stroke();
			} else if (kind === 'liashock') {
				ctx.ellipse(128, 176, 16, 22, 0, 0, Math.PI * 2);
				ctx.fill();
			} else {
				ctx.arc(128, 196, 22, Math.PI * 1.2, Math.PI * 1.8);
				ctx.stroke();
				ctx.beginPath();
				ctx.moveTo(66, 80);
				ctx.lineTo(104, 70);
				ctx.moveTo(190, 80);
				ctx.lineTo(152, 70);
				ctx.stroke();
			}
			return true;
		}
		case 'liacry': {
			blush(0.75);
			ctx.strokeStyle = ink;
			ctx.lineWidth = 9;
			for (const x of [92, 164]) {
				ctx.beginPath();
				ctx.arc(x, 100, 18, Math.PI * 0.15, Math.PI * 0.85);
				ctx.stroke();
			}
			// tear streams
			ctx.fillStyle = 'rgba(90,180,255,0.95)';
			for (const x of [84, 172]) ctx.fillRect(x - 7, 116, 14, 120);
			ctx.lineWidth = 8;
			ctx.beginPath();
			ctx.moveTo(100, 196);
			ctx.quadraticCurveTo(114, 176, 128, 190);
			ctx.quadraticCurveTo(142, 176, 156, 196);
			ctx.stroke();
			return true;
		}
		case 'hearts': {
			blush(0.8);
			ctx.fillStyle = '#ff2d6f';
			heartPath(ctx, 90, 108, 26);
			heartPath(ctx, 166, 108, 26);
			ctx.strokeStyle = ink;
			ctx.lineWidth = 8;
			ctx.beginPath();
			ctx.arc(128, 150, 26, Math.PI * 0.12, Math.PI * 0.88);
			ctx.stroke();
			return true;
		}
		case 'angry': {
			ctx.fillStyle = ink;
			ctx.strokeStyle = ink;
			for (const x of [92, 164]) {
				ctx.beginPath();
				ctx.ellipse(x, 112, 13, 13, 0, 0, Math.PI * 2);
				ctx.fill();
			}
			ctx.lineWidth = 12;
			ctx.beginPath();
			ctx.moveTo(62, 72);
			ctx.lineTo(112, 92);
			ctx.moveTo(194, 72);
			ctx.lineTo(144, 92);
			ctx.stroke();
			ctx.lineWidth = 9;
			ctx.beginPath();
			ctx.moveTo(92, 186);
			ctx.lineTo(164, 176);
			ctx.stroke();
			return true;
		}
		case 'duck':
		case 'duckwink': {
			// BoompjeJunior's skin face: black pixel eyes, little orange beak, pink cheeks
			const px = 256 / 8;
			ctx.fillStyle = '#1b1320';
			ctx.fillRect(1.5 * px, 3.6 * px, px, kind === 'duckwink' ? px * 0.35 : px);
			ctx.fillRect(5.5 * px, 3.6 * px, px, px);
			ctx.fillStyle = 'rgba(255,120,160,0.75)';
			ctx.fillRect(0.6 * px, 4.9 * px, px, px * 0.6);
			ctx.fillRect(6.4 * px, 4.9 * px, px, px * 0.6);
			ctx.fillStyle = '#ff9a2e';
			ctx.fillRect(3.1 * px, 4.7 * px, px * 1.8, px * 0.75);
			ctx.fillStyle = '#e06d10';
			ctx.fillRect(3.1 * px, 5.3 * px, px * 1.8, px * 0.18);
			return true;
		}
		case 'shock': {
			ctx.fillStyle = '#fff';
			ctx.strokeStyle = ink;
			ctx.lineWidth = 6;
			for (const x of [92, 164]) {
				ctx.beginPath();
				ctx.arc(x, 104, 24, 0, Math.PI * 2);
				ctx.fill();
				ctx.stroke();
				ctx.fillStyle = ink;
				ctx.beginPath();
				ctx.arc(x, 104, 7, 0, Math.PI * 2);
				ctx.fill();
				ctx.fillStyle = '#fff';
			}
			ctx.fillStyle = ink;
			ctx.beginPath();
			ctx.ellipse(128, 182, 20, 26, 0, 0, Math.PI * 2);
			ctx.fill();
			return true;
		}
		case 'sick': {
			ctx.fillStyle = 'rgba(120,200,60,0.55)';
			ctx.fillRect(40, 60, 176, 150);
			ctx.strokeStyle = ink;
			ctx.lineWidth = 9;
			for (const x of [92, 164]) {
				ctx.beginPath();
				ctx.moveTo(x - 16, 96);
				ctx.lineTo(x + 16, 112);
				ctx.moveTo(x - 16, 112);
				ctx.lineTo(x + 16, 96);
				ctx.stroke();
			}
			ctx.beginPath();
			ctx.moveTo(90, 182);
			for (let i = 0; i <= 6; i++) ctx.lineTo(90 + i * 13, 182 + (i % 2 ? -10 : 6));
			ctx.stroke();
			return true;
		}
		case 'kliwide': {
			// kli's pixel smile but the eyes went wide
			ctx.fillStyle = '#ffffff';
			const px = 256 / 8;
			for (const [x, y] of [[1, 5], [6, 5], [2, 6], [3, 6], [4, 6], [5, 6]] as [number, number][]) ctx.fillRect(x * px, y * px - px * 1.2, px, px);
			ctx.fillRect(1.5 * px, 1.6 * px, px * 0.9, px * 0.9);
			ctx.fillRect(5.6 * px, 1.6 * px, px * 0.9, px * 0.9);
			return true;
		}
		default:
			return false;
	}
};

export const shirtTexture = (kind: 'req' | 'plain' | 'stripe' | 'heart' | 'suit' | 'abs' | 'lia' | 'yf' | 'kid', color = '#fff') =>
	canvasTex('shirt-' + kind + color, 256, 256, (ctx) => {
		ctx.clearRect(0, 0, 256, 256);
		if (kind === 'abs') {
			// cartoon muscle shirt: pecs + six pack, a little duck badge and a tiny dutch flag
			ctx.strokeStyle = color;
			ctx.lineWidth = 7;
			ctx.lineCap = 'round';
			ctx.beginPath();
			ctx.moveTo(40, 40);
			ctx.quadraticCurveTo(84, 104, 126, 66);
			ctx.moveTo(216, 40);
			ctx.quadraticCurveTo(172, 104, 130, 66);
			ctx.moveTo(128, 70);
			ctx.lineTo(128, 236);
			for (const y of [130, 170, 208]) {
				ctx.moveTo(86, y);
				ctx.quadraticCurveTo(106, y + 8, 124, y);
				ctx.moveTo(132, y);
				ctx.quadraticCurveTo(150, y + 8, 170, y);
			}
			ctx.stroke();
			const fx = 178;
			const fy = 14;
			['#ae1c28', '#ffffff', '#21468b'].forEach((c, i) => {
				ctx.fillStyle = c;
				ctx.fillRect(fx, fy + i * 10, 46, 10);
			});
			return;
		}
		if (kind === 'lia') {
			ctx.fillStyle = '#ffffff';
			heartPath(ctx, 128, 112, 46);
			ctx.fillStyle = '#ff4fa3';
			heartPath(ctx, 128, 112, 30);
			ctx.fillStyle = '#fff6a8';
			for (const [x, y, r] of [[56, 60, 10], [204, 74, 8], [196, 190, 11], [62, 182, 7]] as const) {
				ctx.beginPath();
				for (let k = 0; k < 8; k++) {
					const a = (k / 8) * Math.PI * 2;
					const rr = k % 2 ? r * 0.4 : r;
					ctx.lineTo(x + Math.cos(a) * rr, y + Math.sin(a) * rr);
				}
				ctx.fill();
			}
			return;
		}
		if (kind === 'yf') {
			ctx.font = '900 110px "Fredoka", sans-serif';
			ctx.textAlign = 'center';
			ctx.textBaseline = 'middle';
			ctx.fillStyle = '#e53935';
			ctx.fillText('YF', 128, 120);
			ctx.fillStyle = 'rgba(0,0,0,0.25)';
			ctx.fillRect(56, 186, 144, 46);
			return;
		}
		if (kind === 'kid') {
			ctx.fillStyle = '#ffffff';
			heartPath(ctx, 128, 118, 36);
			return;
		}
		if (kind === 'req') {
			// hoodie strings
			ctx.strokeStyle = '#e8e8e8';
			ctx.lineWidth = 7;
			ctx.beginPath();
			ctx.moveTo(108, 0);
			ctx.lineTo(104, 70);
			ctx.moveTo(148, 0);
			ctx.lineTo(152, 70);
			ctx.stroke();
			// pocket
			ctx.fillStyle = 'rgba(0,0,0,0.18)';
			ctx.fillRect(56, 168, 144, 64);
			// gold coin logo with $
			const g = ctx.createRadialGradient(118, 108, 6, 128, 118, 46);
			g.addColorStop(0, '#fff3a6');
			g.addColorStop(0.5, '#ffcc33');
			g.addColorStop(1, '#c98a00');
			ctx.fillStyle = g;
			ctx.beginPath();
			ctx.arc(128, 118, 40, 0, Math.PI * 2);
			ctx.fill();
			ctx.fillStyle = '#7a4a00';
			ctx.font = 'bold 58px sans-serif';
			ctx.textAlign = 'center';
			ctx.textBaseline = 'middle';
			ctx.fillText('$', 128, 121);
		} else if (kind === 'stripe') {
			ctx.fillStyle = color;
			for (let y = 20; y < 256; y += 56) ctx.fillRect(0, y, 256, 22);
		} else if (kind === 'heart') {
			ctx.fillStyle = color;
			ctx.beginPath();
			ctx.moveTo(128, 170);
			ctx.bezierCurveTo(60, 120, 80, 60, 128, 92);
			ctx.bezierCurveTo(176, 60, 196, 120, 128, 170);
			ctx.fill();
		} else if (kind === 'suit') {
			// white shirt + bow tie (wedding)
			ctx.fillStyle = '#ffffff';
			ctx.beginPath();
			ctx.moveTo(96, 0);
			ctx.lineTo(160, 0);
			ctx.lineTo(128, 150);
			ctx.closePath();
			ctx.fill();
			ctx.fillStyle = color;
			ctx.beginPath();
			ctx.moveTo(128, 30);
			ctx.lineTo(98, 14);
			ctx.lineTo(98, 46);
			ctx.closePath();
			ctx.moveTo(128, 30);
			ctx.lineTo(158, 14);
			ctx.lineTo(158, 46);
			ctx.closePath();
			ctx.fill();
		}
	});

export const grassTexture = () =>
	canvasTex(
		'grass',
		512,
		512,
		(ctx) => {
			ctx.fillStyle = '#4fa13a';
			ctx.fillRect(0, 0, 512, 512);
			for (let i = 0; i < 9000; i++) {
				const x = rand(i) * 512;
				const y = rand(i + 0.5) * 512;
				const l = rand(i + 0.25);
				ctx.fillStyle = l > 0.5 ? 'rgba(120,200,80,0.35)' : 'rgba(30,90,25,0.35)';
				ctx.fillRect(x, y, 2 + l * 3, 2 + l * 3);
			}
		},
		{repeat: [80, 80]},
	);

// Roblox "baseplate" style tiles with faint stud grid
export const tileTexture = (base: string, line: string, key: string) =>
	canvasTex(
		'tile-' + key,
		256,
		256,
		(ctx) => {
			ctx.fillStyle = base;
			ctx.fillRect(0, 0, 256, 256);
			for (let i = 0; i < 1600; i++) {
				ctx.fillStyle = rand(i * 3.1) > 0.5 ? 'rgba(255,255,255,0.05)' : 'rgba(0,0,0,0.06)';
				ctx.fillRect(rand(i) * 256, rand(i + 9) * 256, 3, 3);
			}
			ctx.strokeStyle = line;
			ctx.lineWidth = 4;
			ctx.strokeRect(2, 2, 252, 252);
		},
		{repeat: [1, 1]},
	);

export const checkerTexture = () =>
	canvasTex(
		'checker',
		256,
		256,
		(ctx) => {
			ctx.fillStyle = '#5b2a86';
			ctx.fillRect(0, 0, 256, 256);
			ctx.fillStyle = '#3a1660';
			ctx.fillRect(0, 0, 128, 128);
			ctx.fillRect(128, 128, 128, 128);
			ctx.strokeStyle = 'rgba(255,210,80,0.5)';
			ctx.lineWidth = 3;
			ctx.strokeRect(0, 0, 256, 256);
		},
		{repeat: [8, 8]},
	);

export const SYMBOLS = ['🐱', '💎', '7', '🐶', '💀', '🍀'];

// a vertical strip of slot symbols, used with texture.offset.y to spin
export const reelTexture = () => {
	const key = 'reel';
	const hit = cache.get(key);
	if (hit) return hit;
	const c = document.createElement('canvas');
	const S = 256;
	c.width = S;
	c.height = S * SYMBOLS.length;
	const ctx = c.getContext('2d')!;
	SYMBOLS.forEach((s, i) => {
		ctx.fillStyle = i % 2 ? '#fff8e8' : '#ffffff';
		ctx.fillRect(0, i * S, S, S);
		ctx.font = s === '7' ? `bold ${S * 0.75}px sans-serif` : `${S * 0.66}px "Noto Color Emoji"`;
		ctx.fillStyle = '#e0242c';
		ctx.textAlign = 'center';
		ctx.textBaseline = 'middle';
		ctx.fillText(s, S / 2, i * S + S * 0.55);
	});
	const t = new THREE.CanvasTexture(c);
	t.colorSpace = THREE.SRGBColorSpace;
	t.wrapS = t.wrapT = THREE.RepeatWrapping;
	t.repeat.set(1, 1 / SYMBOLS.length);
	cache.set(key, t);
	return t;
};

export const signTexture = (text: string, bg: string, fg: string, key: string, w = 1024, h = 256) =>
	canvasTex('sign-' + key, w, h, (ctx) => {
		const g = ctx.createLinearGradient(0, 0, 0, h);
		g.addColorStop(0, bg);
		g.addColorStop(1, '#000');
		ctx.fillStyle = g;
		ctx.fillRect(0, 0, w, h);
		ctx.font = `900 ${h * 0.55}px "Fredoka", sans-serif`;
		ctx.textAlign = 'center';
		ctx.textBaseline = 'middle';
		ctx.lineWidth = h * 0.06;
		ctx.strokeStyle = '#3b1600';
		ctx.strokeText(text, w / 2, h * 0.54);
		ctx.fillStyle = fg;
		ctx.fillText(text, w / 2, h * 0.54);
	});

export const spawnTexture = () =>
	canvasTex('spawn', 256, 256, (ctx) => {
		ctx.fillStyle = '#a3a2a5';
		ctx.fillRect(0, 0, 256, 256);
		ctx.strokeStyle = '#7f7f82';
		ctx.lineWidth = 10;
		ctx.strokeRect(10, 10, 236, 236);
		// classic spawn decal: circle + cross
		ctx.strokeStyle = '#d8d8da';
		ctx.lineWidth = 14;
		ctx.beginPath();
		ctx.arc(128, 128, 70, 0, Math.PI * 2);
		ctx.stroke();
		ctx.beginPath();
		ctx.moveTo(128, 40);
		ctx.lineTo(128, 216);
		ctx.moveTo(40, 128);
		ctx.lineTo(216, 128);
		ctx.stroke();
	});
