import React, {useMemo} from 'react';
import * as THREE from 'three';
import {rbox} from './Avatar';
import {V3} from './cam';
import {canvasTex, rand} from './textures';
import {Env} from './World';

// ---------------------------------------------------------------- textures
const planksTexture = () =>
	canvasTex(
		'planks',
		512,
		512,
		(ctx) => {
			const cols = ['#7a4a2a', '#6e4224', '#82512e', '#744628', '#6a3f22'];
			for (let r = 0; r < 8; r++) {
				let x = -rand(r) * 200;
				while (x < 512) {
					const w = 160 + rand(r * 7 + x) * 160;
					ctx.fillStyle = cols[Math.floor(rand(r * 3.3 + x * 0.1) * cols.length)];
					ctx.fillRect(x, r * 64, w, 64);
					for (let g = 0; g < 6; g++) {
						ctx.fillStyle = 'rgba(40,20,8,0.12)';
						ctx.fillRect(x, r * 64 + 6 + g * 10 + rand(g + r) * 4, w, 2);
					}
					ctx.fillStyle = 'rgba(20,10,4,0.65)';
					ctx.fillRect(x, r * 64, 3, 64);
					x += w;
				}
				ctx.fillStyle = 'rgba(20,10,4,0.7)';
				ctx.fillRect(0, r * 64, 512, 3);
			}
		},
		{repeat: [6, 6]},
	);

const wallpaperTexture = () =>
	canvasTex(
		'wallpaper',
		256,
		256,
		(ctx) => {
			ctx.fillStyle = '#5b2130';
			ctx.fillRect(0, 0, 256, 256);
			ctx.fillStyle = 'rgba(255,215,140,0.16)';
			for (let i = 0; i < 4; i++) {
				const x = 32 + (i % 2) * 128;
				const y = 32 + Math.floor(i / 2) * 128;
				ctx.beginPath();
				ctx.moveTo(x + 32, y);
				ctx.quadraticCurveTo(x + 64, y + 32, x + 32, y + 64);
				ctx.quadraticCurveTo(x, y + 32, x + 32, y);
				ctx.fill();
			}
			ctx.fillStyle = 'rgba(0,0,0,0.12)';
			for (let x = 0; x < 256; x += 64) ctx.fillRect(x, 0, 4, 256);
		},
		{repeat: [10, 2]},
	);

const stoneTexture = () =>
	canvasTex(
		'stone',
		256,
		256,
		(ctx) => {
			ctx.fillStyle = '#8d8f94';
			ctx.fillRect(0, 0, 256, 256);
			for (let i = 0; i < 4; i++)
				for (let j = 0; j < 4; j++) {
					const v = 128 + Math.floor((rand(i * 4 + j) - 0.5) * 30);
					ctx.fillStyle = `rgb(${v + 5},${v + 7},${v + 12})`;
					ctx.fillRect(i * 64 + 2, j * 64 + 2, 60, 60);
				}
			for (let n = 0; n < 1400; n++) {
				ctx.fillStyle = rand(n * 1.7) > 0.5 ? 'rgba(255,255,255,0.05)' : 'rgba(0,0,0,0.07)';
				ctx.fillRect(rand(n) * 256, rand(n + 4) * 256, 3, 3);
			}
		},
		{repeat: [16, 16]},
	);

const screenTexture = () =>
	canvasTex('mm2screen', 1024, 512, (ctx) => {
		const g = ctx.createLinearGradient(0, 0, 0, 512);
		g.addColorStop(0, '#1a0006');
		g.addColorStop(1, '#000');
		ctx.fillStyle = g;
		ctx.fillRect(0, 0, 1024, 512);
		ctx.textAlign = 'center';
		ctx.textBaseline = 'middle';
		ctx.font = '900 120px "Fredoka", sans-serif';
		ctx.lineWidth = 14;
		ctx.strokeStyle = '#000';
		ctx.strokeText('MURDER', 512, 130);
		ctx.fillStyle = '#e8e8e8';
		ctx.fillText('MURDER', 512, 130);
		ctx.strokeText('MYSTERY', 512, 260);
		ctx.fillText('MYSTERY', 512, 260);
		ctx.font = '900 150px "Fredoka", sans-serif';
		ctx.fillStyle = '#e01b24';
		ctx.strokeText('2', 512, 400);
		ctx.fillText('2', 512, 400);
		// knife
		ctx.fillStyle = '#cfd6dd';
		ctx.beginPath();
		ctx.moveTo(150, 330);
		ctx.lineTo(330, 300);
		ctx.lineTo(330, 340);
		ctx.closePath();
		ctx.fill();
		ctx.fillStyle = '#5a2e14';
		ctx.fillRect(330, 300, 70, 40);
		// gun
		ctx.fillStyle = '#7d8790';
		ctx.fillRect(650, 300, 180, 36);
		ctx.fillRect(780, 300, 40, 90);
	});

const mapPadTexture = (name: string, color: string) =>
	canvasTex('pad-' + name, 512, 256, (ctx) => {
		ctx.fillStyle = color;
		ctx.fillRect(0, 0, 512, 256);
		ctx.fillStyle = 'rgba(0,0,0,0.25)';
		ctx.fillRect(0, 180, 512, 76);
		ctx.textAlign = 'center';
		ctx.textBaseline = 'middle';
		ctx.font = '900 92px "Fredoka", sans-serif';
		ctx.lineWidth = 12;
		ctx.strokeStyle = '#111';
		ctx.strokeText(name, 256, 96);
		ctx.fillStyle = '#fff';
		ctx.fillText(name, 256, 96);
		ctx.font = '700 50px "Fredoka", sans-serif';
		ctx.lineWidth = 8;
		ctx.strokeText('VOTE', 256, 218);
		ctx.fillText('VOTE', 256, 218);
	});

// ---------------------------------------------------------------- environments
export const LOBBY_DAY: Env = {
	skyTop: '#3a86e8',
	skyHorizon: '#cfe9ff',
	sunDir: [0.5, 0.75, 0.45],
	sunColor: '#fff1dc',
	sunIntensity: 2.5,
	hemiSky: '#d6ebff',
	hemiGround: '#6b7a5a',
	hemiIntensity: 1.0,
	fog: ['#d6ebff', 120, 420],
	sunGlow: 0.6,
};

export const LOBBY_NIGHT: Env = {
	skyTop: '#03050c',
	skyHorizon: '#1a2236',
	sunDir: [-0.3, 0.6, -0.5],
	sunColor: '#8ea8ff',
	sunIntensity: 0.55,
	hemiSky: '#3a4a70',
	hemiGround: '#0b0d14',
	hemiIntensity: 0.45,
	fog: ['#151b2a', 40, 170],
	sunGlow: 0.2,
	stars: 0,
};

export const LOBBY_SUNSET: Env = {
	skyTop: '#4a3a9a',
	skyHorizon: '#ffa3c0',
	sunDir: [-0.15, 0.16, -1],
	sunColor: '#ffb48e',
	sunIntensity: 2.4,
	hemiSky: '#ffc4d6',
	hemiGround: '#55405a',
	hemiIntensity: 0.85,
	fog: ['#f6acc0', 110, 420],
	sunGlow: 1.7,
};

export const TOXIC: Env = {
	skyTop: '#0e2205',
	skyHorizon: '#8bd12a',
	sunDir: [0.2, 0.3, -1],
	sunColor: '#c6ff5a',
	sunIntensity: 2.0,
	hemiSky: '#a5ff4f',
	hemiGround: '#1d2a0a',
	hemiIntensity: 0.8,
	fog: ['#6c9c22', 30, 160],
	sunGlow: 1.4,
};

export const INDOOR: Env = {
	skyTop: '#0b1020',
	skyHorizon: '#1a2240',
	sunDir: [0.35, 1, 0.55],
	sunColor: '#ffe2bd',
	sunIntensity: 1.1,
	hemiSky: '#ffd9b0',
	hemiGround: '#3a2418',
	hemiIntensity: 0.75,
	fog: ['#1a1410', 80, 300],
	sunGlow: 0,
	shadowCenter: [0, 0, 0],
	shadowSize: 22,
};

export const SPACE: Env = {
	skyTop: '#000004',
	skyHorizon: '#050816',
	sunDir: [1, 0.3, 0.6],
	sunColor: '#fff2dd',
	sunIntensity: 3.0,
	hemiSky: '#334',
	hemiGround: '#000',
	hemiIntensity: 0.25,
	fog: ['#000', 900, 2000],
	sunGlow: 0.8,
	stars: 1.6,
};

// ---------------------------------------------------------------- lobby
export const Lamp: React.FC<{position: V3; on?: number}> = ({position, on = 1}) => (
	<group position={position}>
		<mesh position={[0, 3.5, 0]} castShadow>
			<cylinderGeometry args={[0.16, 0.24, 7, 10]} />
			<meshStandardMaterial color="#26262b" metalness={0.6} roughness={0.4} />
		</mesh>
		<mesh position={[0, 7.3, 0]}>
			<boxGeometry args={[0.8, 0.9, 0.8]} />
			<meshStandardMaterial color="#fff1c4" emissive="#ffc46b" emissiveIntensity={3 * on} />
		</mesh>
		{on > 0 ? <pointLight position={[0, 6.6, 0]} color="#ffbe6b" intensity={120 * on} distance={20} decay={1.6} /> : null}
	</group>
);

export const LobbyBench: React.FC<{position: V3; rotationY?: number}> = ({position, rotationY = 0}) => (
	<group position={position} rotation={[0, rotationY, 0]}>
		<mesh position={[0, 1.0, 0]} geometry={rbox(7, 0.35, 1.6, 0.08)} castShadow receiveShadow>
			<meshStandardMaterial color="#8a5a34" roughness={0.8} />
		</mesh>
		<mesh position={[0, 2.0, -0.8]} geometry={rbox(7, 1.6, 0.3, 0.08)} castShadow>
			<meshStandardMaterial color="#8a5a34" roughness={0.8} />
		</mesh>
		{[-3, 3].map((x) => (
			<mesh key={x} position={[x, 0.5, 0]} geometry={rbox(0.3, 1, 1.4, 0.05)} castShadow>
				<meshStandardMaterial color="#2b2b30" metalness={0.5} roughness={0.5} />
			</mesh>
		))}
	</group>
);

const LowTree: React.FC<{position: V3; s?: number; seed?: number}> = ({position, s = 1, seed = 0}) => {
	const leaf = ['#3e9b3a', '#4caf50', '#2e7d32'][seed % 3];
	return (
		<group position={position} scale={s} rotation={[0, seed, 0]}>
			<mesh position={[0, 3, 0]} geometry={rbox(1.4, 6, 1.4, 0.15)} castShadow>
				<meshStandardMaterial color="#7a5230" roughness={0.9} />
			</mesh>
			<mesh position={[0, 7.4, 0]} castShadow>
				<icosahedronGeometry args={[3.6, 0]} />
				<meshStandardMaterial color={leaf} roughness={0.85} flatShading />
			</mesh>
			<mesh position={[1.6, 6.2, 0.8]} castShadow>
				<icosahedronGeometry args={[2.2, 0]} />
				<meshStandardMaterial color={leaf} roughness={0.85} flatShading />
			</mesh>
		</group>
	);
};

/** MM2-style lobby plaza, centered at origin. Plaza is 56 x 56. Big screen at z = -27. */
export const Lobby: React.FC<{lampsOn?: number; t?: number}> = ({lampsOn = 0, t = 0}) => {
	const stone = useMemo(() => stoneTexture(), []);
	const screen = useMemo(() => screenTexture(), []);
	const pads = useMemo(
		() => [
			{name: 'Mansion', c: '#7b2d8b', x: -14},
			{name: 'Factory', c: '#c0392b', x: 0},
			{name: 'Hotel', c: '#2471a3', x: 14},
		],
		[],
	);
	const trees = useMemo(() => {
		const out: {p: V3; s: number; i: number}[] = [];
		for (let i = 0; out.length < 36 && i < 300; i++) {
			const a = rand(i * 3.1) * Math.PI * 2;
			const r = 40 + rand(i * 7.7) * 120;
			const x = Math.cos(a) * r;
			const z = Math.sin(a) * r;
			if (Math.abs(x) < 36 && Math.abs(z) < 36) continue;
			out.push({p: [x, 0, z], s: 0.8 + rand(i) * 0.7, i});
		}
		return out;
	}, []);
	return (
		<>
			{/* grass */}
			<mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -0.02, 0]} receiveShadow>
				<planeGeometry args={[900, 900]} />
				<meshStandardMaterial color="#4f9a3a" roughness={0.95} />
			</mesh>
			{/* plaza */}
			<mesh position={[0, 0.2, 0]} geometry={rbox(56, 0.4, 56, 0.1)} receiveShadow>
				<meshStandardMaterial map={stone} roughness={0.85} />
			</mesh>
			{/* low walls with gaps */}
			{[
				[-28, 0, 0.6, 56],
				[28, 0, 0.6, 56],
				[-17, 28, 22, 0.6],
				[17, 28, 22, 0.6],
			].map(([x, z, w, d], i) => (
				<mesh key={i} position={[x, 1.2, z]} geometry={rbox(w + 0.4, 2, d + 0.4, 0.1)} castShadow receiveShadow>
					<meshStandardMaterial color="#6d6f75" roughness={0.9} />
				</mesh>
			))}
			{/* big screen */}
			<group position={[0, 0, -27]}>
				<mesh position={[0, 9, -0.6]} geometry={rbox(30, 15, 1, 0.2)} castShadow>
					<meshStandardMaterial color="#1b1b1f" roughness={0.6} />
				</mesh>
				<mesh position={[0, 9, 0]}>
					<planeGeometry args={[28, 13.5]} />
					<meshStandardMaterial map={screen} emissive="#ffffff" emissiveMap={screen} emissiveIntensity={0.8} />
				</mesh>
				{[-12, 12].map((x) => (
					<mesh key={x} position={[x, 1, -0.6]} geometry={rbox(1.2, 2, 1.2, 0.1)}>
						<meshStandardMaterial color="#1b1b1f" />
					</mesh>
				))}
			</group>
			{/* map vote pads */}
			{pads.map((p) => (
				<group key={p.name} position={[p.x, 0.4, -15]}>
					<mesh position={[0, 0.15, 0]} geometry={rbox(9, 0.3, 6, 0.1)} receiveShadow>
						<meshStandardMaterial color={p.c} roughness={0.5} emissive={p.c} emissiveIntensity={0.25 + 0.2 * Math.sin(t * 3 + p.x)} />
					</mesh>
					<mesh position={[0, 3.6, -3.2]}>
						<planeGeometry args={[7, 3.5]} />
						<meshStandardMaterial map={mapPadTexture(p.name, p.c)} emissive="#ffffff" emissiveMap={mapPadTexture(p.name, p.c)} emissiveIntensity={0.35} />
					</mesh>
					<mesh position={[0, 1.0, -3.3]} geometry={rbox(0.3, 2, 0.3, 0.05)}>
						<meshStandardMaterial color="#222" />
					</mesh>
				</group>
			))}
			{/* benches + lamps + crates */}
			<LobbyBench position={[-18, 0.4, 10]} rotationY={Math.PI / 2} />
			<LobbyBench position={[18, 0.4, 10]} rotationY={-Math.PI / 2} />
			<LobbyBench position={[0, 0.4, 20]} rotationY={Math.PI} />
			{[
				[-24, 24],
				[24, 24],
				[-24, -6],
				[24, -6],
				[-8, 22],
				[8, 22],
			].map(([x, z], i) => (
				<Lamp key={i} position={[x, 0.4, z]} on={lampsOn} />
			))}
			{[
				[-24, 0.4, -22],
				[-22.2, 0.4, -22.6],
				[-23.2, 2.2, -22.2],
				[24, 0.4, 16],
			].map(([x, y, z], i) => (
				<mesh key={i} position={[x, y + 0.9, z]} rotation={[0, i * 0.4, 0]} geometry={rbox(1.8, 1.8, 1.8, 0.08)} castShadow>
					<meshStandardMaterial color="#a0703e" roughness={0.9} />
				</mesh>
			))}
			{trees.map((tr) => (
				<LowTree key={tr.i} position={tr.p} s={tr.s} seed={tr.i} />
			))}
		</>
	);
};

// ---------------------------------------------------------------- mansion (MM2 map)
const Sofa: React.FC<{position: V3; rotationY?: number; color?: string; w?: number}> = ({position, rotationY = 0, color = '#7b1e2b', w = 7}) => (
	<group position={position} rotation={[0, rotationY, 0]}>
		<mesh position={[0, 0.9, 0]} geometry={rbox(w, 1.2, 2.6, 0.3)} castShadow receiveShadow>
			<meshStandardMaterial color={color} roughness={0.8} />
		</mesh>
		<mesh position={[0, 2.1, -1.0]} geometry={rbox(w, 2.2, 0.7, 0.3)} castShadow>
			<meshStandardMaterial color={color} roughness={0.8} />
		</mesh>
		{[-1, 1].map((s) => (
			<mesh key={s} position={[s * (w / 2 - 0.35), 1.6, 0]} geometry={rbox(0.7, 1.6, 2.6, 0.3)} castShadow>
				<meshStandardMaterial color={color} roughness={0.8} />
			</mesh>
		))}
	</group>
);

const Painting: React.FC<{position: V3; rotationY?: number; colors: string[]}> = ({position, rotationY = 0, colors}) => {
	const tex = useMemo(
		() =>
			canvasTex('paint-' + colors.join(), 256, 192, (ctx) => {
				const g = ctx.createLinearGradient(0, 0, 0, 192);
				g.addColorStop(0, colors[0]);
				g.addColorStop(1, colors[1]);
				ctx.fillStyle = g;
				ctx.fillRect(0, 0, 256, 192);
				ctx.fillStyle = colors[2];
				ctx.beginPath();
				ctx.arc(170, 70, 30, 0, Math.PI * 2);
				ctx.fill();
				ctx.fillStyle = 'rgba(0,0,0,0.35)';
				ctx.beginPath();
				ctx.moveTo(0, 192);
				ctx.lineTo(80, 110);
				ctx.lineTo(150, 160);
				ctx.lineTo(210, 120);
				ctx.lineTo(256, 192);
				ctx.fill();
			}),
		[colors],
	);
	return (
		<group position={position} rotation={[0, rotationY, 0]}>
			<mesh geometry={rbox(4.6, 3.6, 0.25, 0.06)}>
				<meshStandardMaterial color="#c9a227" metalness={0.7} roughness={0.35} />
			</mesh>
			<mesh position={[0, 0, 0.14]}>
				<planeGeometry args={[4, 3]} />
				<meshStandardMaterial map={tex} roughness={0.7} />
			</mesh>
		</group>
	);
};

export const Coin: React.FC<{position: V3; t: number}> = ({position, t}) => (
	<group position={[position[0], position[1] + 0.9 + Math.sin(t * 3 + position[0]) * 0.15, position[2]]} rotation={[0, t * 3 + position[2], 0]}>
		<mesh rotation={[Math.PI / 2, 0, 0]} castShadow>
			<cylinderGeometry args={[0.55, 0.55, 0.14, 20]} />
			<meshStandardMaterial color="#ffd23f" emissive="#ffb000" emissiveIntensity={0.35} metalness={0.7} roughness={0.25} />
		</mesh>
	</group>
);

/** Mansion living room. Room spans x -18..18, z -14..14, height 12. Door in back wall at x = 9. */
export const Mansion: React.FC<{t: number; doorOpen?: number; fire?: boolean}> = ({t, doorOpen = 0, fire = true}) => {
	const planks = useMemo(() => planksTexture(), []);
	const paper = useMemo(() => wallpaperTexture(), []);
	const flick = 1 + 0.15 * Math.sin(t * 13) + 0.1 * Math.sin(t * 29 + 1);
	const W = 36;
	const D = 28;
	const HGT = 12;
	return (
		<>
			{/* floor */}
			<mesh rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
				<planeGeometry args={[W, D]} />
				<meshStandardMaterial map={planks} roughness={0.55} />
			</mesh>
			{/* rug */}
			<mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0.03, 1]} receiveShadow>
				<planeGeometry args={[16, 10]} />
				<meshStandardMaterial color="#8b1e2e" roughness={0.95} />
			</mesh>
			<mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0.04, 1]} receiveShadow>
				<planeGeometry args={[14.6, 8.6]} />
				<meshStandardMaterial color="#b5893e" roughness={0.95} />
			</mesh>
			<mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0.05, 1]} receiveShadow>
				<planeGeometry args={[13.6, 7.6]} />
				<meshStandardMaterial color="#7a1726" roughness={0.95} />
			</mesh>
			{/* ceiling */}
			<mesh rotation={[Math.PI / 2, 0, 0]} position={[0, HGT, 0]}>
				<planeGeometry args={[W, D]} />
				<meshStandardMaterial color="#e9dfcf" roughness={0.9} />
			</mesh>
			{/* walls: back (with door gap), left, right, front */}
			{(
				[
					[-5.75, -D / 2, 24.5, 0], // back wall left of the door (x -18..6.5)
					[14.75, -D / 2, 6.5, 0], // right of the door (x 11.5..18)
					[-W / 2, 0, D, Math.PI / 2],
					[W / 2, 0, D, -Math.PI / 2],
					[0, D / 2, W, Math.PI],
				] as [number, number, number, number][]
			).map(([x, z, w, ry], i) => (
				<group key={i} position={[x, 0, z]} rotation={[0, ry, 0]}>
					<mesh position={[0, HGT / 2, 0]}>
						<planeGeometry args={[w, HGT]} />
						<meshStandardMaterial map={paper} roughness={0.85} side={THREE.DoubleSide} />
					</mesh>
					<mesh position={[0, 1.6, 0.12]}>
						<boxGeometry args={[w, 3.2, 0.24]} />
						<meshStandardMaterial color="#4a2a17" roughness={0.6} />
					</mesh>
					<mesh position={[0, 3.25, 0.2]}>
						<boxGeometry args={[w, 0.25, 0.3]} />
						<meshStandardMaterial color="#c9a46a" roughness={0.5} />
					</mesh>
					<mesh position={[0, HGT - 0.3, 0.2]}>
						<boxGeometry args={[w, 0.6, 0.4]} />
						<meshStandardMaterial color="#efe6d6" roughness={0.6} />
					</mesh>
				</group>
			))}
			{/* above-door piece */}
			<mesh position={[9, 10.25, -D / 2]}>
				<planeGeometry args={[5, 3.5]} />
				<meshStandardMaterial map={paper} roughness={0.85} side={THREE.DoubleSide} />
			</mesh>
			{/* door frame + door */}
			<group position={[9, 0, -D / 2]}>
				{[-2.6, 2.6].map((x) => (
					<mesh key={x} position={[x, 4.25, 0.15]} geometry={rbox(0.5, 8.5, 0.5, 0.05)}>
						<meshStandardMaterial color="#efe6d6" />
					</mesh>
				))}
				<mesh position={[0, 8.6, 0.15]} geometry={rbox(5.7, 0.5, 0.5, 0.05)}>
					<meshStandardMaterial color="#efe6d6" />
				</mesh>
				<group position={[-2.35, 0, 0]} rotation={[0, -doorOpen * 1.6, 0]}>
					<mesh position={[2.35, 4.25, 0]} geometry={rbox(4.6, 8.4, 0.3, 0.05)} castShadow>
						<meshStandardMaterial color="#5a321a" roughness={0.6} />
					</mesh>
					<mesh position={[4.1, 4.2, 0.25]}>
						<sphereGeometry args={[0.2, 12, 8]} />
						<meshStandardMaterial color="#d4af37" metalness={0.8} roughness={0.3} />
					</mesh>
				</group>
				{/* dark hallway behind */}
				<mesh position={[0, 4.25, -3]}>
					<boxGeometry args={[5, 8.5, 0.2]} />
					<meshStandardMaterial color="#120c08" />
				</mesh>
			</group>
			{/* windows on left wall */}
			{[-7, 5].map((z) => (
				<group key={z} position={[-W / 2 + 0.05, 6.4, z]} rotation={[0, Math.PI / 2, 0]}>
					<mesh>
						<planeGeometry args={[5, 6]} />
						<meshStandardMaterial color="#1b2a55" emissive="#2a4fa0" emissiveIntensity={0.7} />
					</mesh>
					<mesh position={[0, 0, 0.1]}>
						<boxGeometry args={[0.25, 6, 0.2]} />
						<meshStandardMaterial color="#efe6d6" />
					</mesh>
					<mesh position={[0, 0, 0.1]}>
						<boxGeometry args={[5, 0.25, 0.2]} />
						<meshStandardMaterial color="#efe6d6" />
					</mesh>
					<mesh position={[0, 0, 0.05]}>
						<boxGeometry args={[5.6, 6.6, 0.1]} />
						<meshStandardMaterial color="#efe6d6" />
					</mesh>
					{/* curtains */}
					{[-1, 1].map((s) => (
						<mesh key={s} position={[s * 3.2, 0, 0.3]} geometry={rbox(1.2, 7.4, 0.3, 0.1)}>
							<meshStandardMaterial color="#6e1020" roughness={0.9} />
						</mesh>
					))}
				</group>
			))}
			{/* fireplace on right wall */}
			<group position={[W / 2 - 0.8, 0, -2]} rotation={[0, -Math.PI / 2, 0]}>
				<mesh position={[0, 3, 0]} geometry={rbox(8, 6, 1.6, 0.1)} castShadow>
					<meshStandardMaterial color="#9a9188" roughness={0.9} />
				</mesh>
				<mesh position={[0, 2, 0.55]} geometry={rbox(4.4, 3.4, 0.6, 0.05)}>
					<meshStandardMaterial color="#120a06" />
				</mesh>
				<mesh position={[0, 6.2, 0.2]} geometry={rbox(9, 0.5, 2.2, 0.08)} castShadow>
					<meshStandardMaterial color="#4a2a17" />
				</mesh>
				{fire ? (
					<>
						{[-0.8, 0, 0.8].map((x, i) => (
							<mesh key={x} position={[x, 1.2 + 0.2 * Math.sin(t * 9 + i), 0.9]} scale={[1, 1 + 0.25 * Math.sin(t * 11 + i * 2), 1]}>
								<coneGeometry args={[0.55, 1.8, 6]} />
								<meshBasicMaterial color={i === 1 ? '#ffd27a' : '#ff7a1a'} />
							</mesh>
						))}
						<pointLight position={[0, 2, 2.5]} color="#ff8a3a" intensity={110 * flick} distance={26} decay={1.6} />
					</>
				) : null}
			</group>
			<Painting position={[W / 2 - 0.2, 8.6, -2]} rotationY={-Math.PI / 2} colors={['#ffb36b', '#6b3b8f', '#fff2a8']} />
			<Painting position={[-6, 7, -D / 2 + 0.2]} colors={['#5fa8d3', '#1b4965', '#ffffff']} />
			<Painting position={[-W / 2 + 0.2, 7, -0.8]} rotationY={Math.PI / 2} colors={['#9ad18b', '#2d6a4f', '#ffd166']} />
			{/* bookshelf */}
			<group position={[-13, 0, -D / 2 + 1]}>
				<mesh position={[0, 4.5, 0]} geometry={rbox(6, 9, 1.6, 0.06)} castShadow>
					<meshStandardMaterial color="#3d2212" />
				</mesh>
				{[1.4, 3.6, 5.8, 8.0].map((y, r) =>
					new Array(9).fill(0).map((_, i) => (
						<mesh key={r + '_' + i} position={[-2.4 + i * 0.6, y + 0.5, 0.5]} geometry={rbox(0.45, 1.4 - rand(i + r) * 0.4, 0.9, 0.03)}>
							<meshStandardMaterial color={['#8e2a2a', '#2a5d8e', '#2e7d32', '#c9a227', '#5b3a8e'][(i + r) % 5]} />
						</mesh>
					)),
				)}
			</group>
			{/* sofas + table */}
			<Sofa position={[0, 0, -4.5]} />
			<Sofa position={[-7.5, 0, 2]} rotationY={Math.PI / 2} w={5} />
			<mesh position={[0, 1.1, 1.4]} geometry={rbox(5, 0.3, 2.6, 0.08)} castShadow receiveShadow>
				<meshStandardMaterial color="#4a2a17" roughness={0.4} />
			</mesh>
			{[-2.1, 2.1].map((x) =>
				[0.4, 2.4].map((z) => (
					<mesh key={x + '_' + z} position={[x, 0.5, z]} geometry={rbox(0.25, 1, 0.25, 0.03)}>
						<meshStandardMaterial color="#3a2010" />
					</mesh>
				)),
			)}
			{/* chandelier */}
			<group position={[0, HGT - 2.6, 1]}>
				<mesh position={[0, 1.4, 0]}>
					<cylinderGeometry args={[0.06, 0.06, 2.4, 6]} />
					<meshStandardMaterial color="#c9a227" metalness={0.8} roughness={0.3} />
				</mesh>
				<mesh rotation={[Math.PI / 2, 0, 0]}>
					<torusGeometry args={[1.6, 0.12, 8, 24]} />
					<meshStandardMaterial color="#c9a227" metalness={0.8} roughness={0.3} />
				</mesh>
				{new Array(6).fill(0).map((_, i) => (
					<mesh key={i} position={[Math.cos((i / 6) * Math.PI * 2) * 1.6, 0.35, Math.sin((i / 6) * Math.PI * 2) * 1.6]}>
						<sphereGeometry args={[0.22, 10, 8]} />
						<meshStandardMaterial color="#fff6dc" emissive="#ffd38a" emissiveIntensity={3} />
					</mesh>
				))}
				<pointLight position={[0, -0.6, 0]} color="#ffd9a0" intensity={260} distance={40} decay={1.5} />
			</group>
			{/* side table + lamp */}
			<group position={[12.5, 0, 8]}>
				<mesh position={[0, 1.2, 0]} geometry={rbox(2, 2.4, 2, 0.08)} castShadow>
					<meshStandardMaterial color="#4a2a17" />
				</mesh>
				<mesh position={[0, 3.3, 0]}>
					<cylinderGeometry args={[0.6, 0.9, 1.2, 12]} />
					<meshStandardMaterial color="#fff1d0" emissive="#ffcf80" emissiveIntensity={1.5} />
				</mesh>
				<pointLight position={[0, 3.3, 0]} color="#ffc070" intensity={50} distance={16} decay={1.6} />
			</group>
		</>
	);
};

// ---------------------------------------------------------------- effects
/** Bright beam of light from the sky. */
export const LightBeam: React.FC<{position: V3; k: number; color?: string; radius?: number}> = ({position, k, color = '#fff3c4', radius = 4.5}) =>
	k <= 0 ? null : (
		<group position={position}>
			<mesh position={[0, 40, 0]}>
				<cylinderGeometry args={[radius * 0.6, radius, 80, 32, 1, true]} />
				<meshBasicMaterial color={color} transparent opacity={0.28 * k} depthWrite={false} side={THREE.DoubleSide} blending={THREE.AdditiveBlending} fog={false} />
			</mesh>
			<mesh position={[0, 40, 0]}>
				<cylinderGeometry args={[radius * 0.3, radius * 0.5, 80, 32, 1, true]} />
				<meshBasicMaterial color="#ffffff" transparent opacity={0.3 * k} depthWrite={false} side={THREE.DoubleSide} blending={THREE.AdditiveBlending} fog={false} />
			</mesh>
			<pointLight position={[0, 6, 2]} color={color} intensity={150 * k} distance={30} decay={1.4} />
		</group>
	);

/** Expanding green fart/gas cloud. r = radius. */
export const GasCloud: React.FC<{center: V3; r: number; t: number; opacity?: number; count?: number}> = ({center, r, t, opacity = 0.5, count = 34}) => {
	if (r <= 0) return null;
	return (
		<group position={center}>
			{new Array(count).fill(0).map((_, i) => {
				const a = rand(i) * Math.PI * 2;
				const e = (rand(i + 3) - 0.3) * 0.9;
				const d = (0.35 + rand(i + 7) * 0.65) * r;
				const s = (0.25 + rand(i + 9) * 0.35) * r * (1 + 0.08 * Math.sin(t * 3 + i));
				return (
					<mesh key={i} position={[Math.cos(a) * d * Math.cos(e), Math.max(s * 0.3, 1.5 + Math.sin(e) * d * 0.6), Math.sin(a) * d * Math.cos(e)]} scale={s}>
						<icosahedronGeometry args={[1, 1]} />
						<meshStandardMaterial
							color={i % 3 ? '#8fdc2a' : '#5fae1a'}
							emissive="#3a7a0a"
							emissiveIntensity={0.4}
							transparent
							opacity={opacity * (0.6 + 0.4 * rand(i + 2))}
							depthWrite={false}
							roughness={1}
							flatShading
						/>
					</mesh>
				);
			})}
		</group>
	);
};

/** Small stink puffs right after the fart (k: seconds since). */
export const StinkPuffs: React.FC<{position: V3; k: number}> = ({position, k}) => {
	if (k < 0 || k > 3.5) return null;
	return (
		<group position={position}>
			{new Array(10).fill(0).map((_, i) => {
				const a = i * 2.4;
				const kk = Math.max(0, k - i * 0.12);
				const s = 0.5 + kk * 1.2;
				return (
					<mesh key={i} position={[Math.cos(a) * kk * 2.2, 2.0 + kk * 1.5, -1.0 - Math.abs(Math.sin(a)) * kk * 2]} scale={s}>
						<icosahedronGeometry args={[1, 1]} />
						<meshStandardMaterial color="#9ae03a" transparent opacity={Math.max(0, 0.75 - kk * 0.2)} depthWrite={false} flatShading />
					</mesh>
				);
			})}
		</group>
	);
};

/** Dutch windmill (for BoompjeJunior's "Dutch."). */
export const Windmill: React.FC<{position: V3; t: number; s?: number; rotationY?: number}> = ({position, t, s = 1, rotationY = 0}) => (
	<group position={position} scale={s} rotation={[0, rotationY, 0]}>
		<mesh position={[0, 7, 0]} castShadow>
			<cylinderGeometry args={[2.6, 4, 14, 8]} />
			<meshStandardMaterial color="#8b5a3c" roughness={0.9} />
		</mesh>
		<mesh position={[0, 15.4, 0]} castShadow>
			<coneGeometry args={[3.2, 3.6, 8]} />
			<meshStandardMaterial color="#3a2a22" roughness={0.9} />
		</mesh>
		<mesh position={[0, 3, 3.75]}>
			<boxGeometry args={[1.6, 3, 0.4]} />
			<meshStandardMaterial color="#2f5d3a" />
		</mesh>
		<group position={[0, 13, 3.4]} rotation={[0, 0, t * 1.4]}>
			{[0, 1, 2, 3].map((i) => (
				<group key={i} rotation={[0, 0, (i * Math.PI) / 2]}>
					<mesh position={[0, 5, 0]} geometry={rbox(2.2, 9, 0.2, 0.05)} castShadow>
						<meshStandardMaterial color="#f2ece2" roughness={0.8} />
					</mesh>
				</group>
			))}
			<mesh rotation={[Math.PI / 2, 0, 0]}>
				<cylinderGeometry args={[0.5, 0.5, 0.8, 12]} />
				<meshStandardMaterial color="#3a2a22" />
			</mesh>
		</group>
	</group>
);

export const Tulips: React.FC<{center: V3; w: number; d: number; rows?: number}> = ({center, w, d, rows = 6}) => {
	const items = useMemo(() => {
		const out: {p: V3; c: string}[] = [];
		const cols = ['#e5383b', '#ffba08', '#ff70a6', '#ffffff', '#9d4edd', '#ff7b00'];
		for (let r = 0; r < rows; r++)
			for (let i = 0; i < Math.round(w / 1.2); i++)
				out.push({p: [center[0] - w / 2 + i * 1.2 + (rand(r * 30 + i) - 0.5) * 0.3, 0, center[2] - d / 2 + (r / Math.max(1, rows - 1)) * d], c: cols[r % cols.length]});
		return out;
	}, [center, w, d, rows]);
	return (
		<>
			{items.map((it, i) => (
				<group key={i} position={it.p}>
					<mesh position={[0, 0.5, 0]}>
						<boxGeometry args={[0.12, 1, 0.12]} />
						<meshStandardMaterial color="#2e7d32" />
					</mesh>
					<mesh position={[0, 1.15, 0]}>
						<cylinderGeometry args={[0.32, 0.18, 0.55, 6]} />
						<meshStandardMaterial color={it.c} roughness={0.6} />
					</mesh>
				</group>
			))}
		</>
	);
};

/** Waving Dutch flag on a pole. */
export const DutchFlag: React.FC<{position: V3; t: number; s?: number}> = ({position, t, s = 1}) => (
	<group position={position} scale={s}>
		<mesh position={[0, 6, 0]}>
			<cylinderGeometry args={[0.12, 0.12, 12, 8]} />
			<meshStandardMaterial color="#ddd" metalness={0.6} roughness={0.3} />
		</mesh>
		{['#ae1c28', '#ffffff', '#21468b'].map((c, i) =>
			new Array(8).fill(0).map((_, j) => (
				<mesh key={i + '_' + j} position={[0.35 + j * 0.6, 11.2 - i * 1.0, Math.sin(t * 6 - j * 0.8) * 0.25 * (j / 7)]} rotation={[0, Math.cos(t * 6 - j * 0.8) * 0.3 * (j / 7), 0]}>
					<boxGeometry args={[0.62, 1.0, 0.05]} />
					<meshStandardMaterial color={c} side={THREE.DoubleSide} />
				</mesh>
			)),
		)}
	</group>
);

// ---------------------------------------------------------------- the planet (Roblox world from space)
type Block = {n: THREE.Vector3; c: THREE.Color; v: number; spin: THREE.Vector3};

export const Planet: React.FC<{k: number; t: number; radius?: number}> = ({k, t, radius = 22}) => {
	const blocks = useMemo(() => {
		const out: Block[] = [];
		const N = 700;
		for (let i = 0; i < N; i++) {
			const y = 1 - (i / (N - 1)) * 2;
			const r = Math.sqrt(1 - y * y);
			const th = i * 2.399963;
			const n = new THREE.Vector3(Math.cos(th) * r, y, Math.sin(th) * r);
			const land = Math.sin(n.x * 4.1) + Math.sin(n.y * 3.3 + 1) + Math.sin(n.z * 5.2 + 2) > 0.4;
			const ice = Math.abs(y) > 0.86;
			const c = new THREE.Color(ice ? '#f2f6ff' : land ? (rand(i) > 0.5 ? '#4caf50' : '#3e9b3a') : rand(i) > 0.5 ? '#1e88e5' : '#1976d2');
			out.push({n, c, v: 0.6 + rand(i * 1.3) * 0.9, spin: new THREE.Vector3(rand(i) - 0.5, rand(i + 1) - 0.5, rand(i + 2) - 0.5).multiplyScalar(6)});
		}
		return out;
	}, []);
	const mesh = useMemo(() => {
		const g = new THREE.BoxGeometry(1, 1, 1);
		const m = new THREE.MeshStandardMaterial({roughness: 0.8, flatShading: true});
		const im = new THREE.InstancedMesh(g, m, blocks.length);
		blocks.forEach((b, i) => im.setColorAt(i, b.c));
		return im;
	}, [blocks]);
	const o = new THREE.Object3D();
	const ex = Math.max(0, k);
	blocks.forEach((b, i) => {
		const d = radius + ex * ex * 0 + ex * 70 * b.v;
		o.position.copy(b.n).multiplyScalar(d);
		o.lookAt(0, 0, 0);
		o.rotateX(ex * b.spin.x);
		o.rotateY(ex * b.spin.y);
		const sz = 3.6 * (1 - Math.min(0.6, ex * 0.25));
		o.scale.set(sz, sz, 2.2);
		o.updateMatrix();
		mesh.setMatrixAt(i, o.matrix);
	});
	mesh.instanceMatrix.needsUpdate = true;
	const fire = ex > 0 ? Math.min(1, ex * 3) : 0;
	return (
		<group rotation={[0.3, t * 0.12, 0]}>
			<primitive object={mesh} />
			{/* molten core */}
			<mesh scale={radius * (0.94 + ex * 0.9)}>
				<icosahedronGeometry args={[1, 3]} />
				<meshBasicMaterial color={ex > 0 ? '#ffb347' : '#2f6f2a'} transparent opacity={ex > 0 ? Math.max(0, 1 - ex * 0.9) : 1} />
			</mesh>
			{ex > 0 ? (
				<>
					<mesh scale={radius * (1 + ex * 3.2)}>
						<icosahedronGeometry args={[1, 3]} />
						<meshBasicMaterial color="#ff6a00" transparent opacity={Math.max(0, 0.7 - ex * 0.5) * fire} blending={THREE.AdditiveBlending} depthWrite={false} />
					</mesh>
					<mesh rotation={[Math.PI / 2 - 0.3, 0, 0]} scale={radius * (1.2 + ex * 6)}>
						<ringGeometry args={[0.92, 1, 96]} />
						<meshBasicMaterial color="#fff1c4" transparent opacity={Math.max(0, 0.9 - ex * 0.6)} side={THREE.DoubleSide} blending={THREE.AdditiveBlending} depthWrite={false} />
					</mesh>
					<pointLight color="#ff8a2a" intensity={4000 * Math.max(0, 1.2 - ex * 0.5)} distance={600} decay={1.2} />
				</>
			) : null}
		</group>
	);
};
