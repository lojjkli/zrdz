import React, {useMemo} from 'react';
import * as THREE from 'three';
import {RoundedBoxGeometry} from 'three/examples/jsm/geometries/RoundedBoxGeometry.js';
import {faceTexture, FaceKind, shirtTexture} from './textures';

const geoCache = new Map<string, THREE.BufferGeometry>();
export const rbox = (w: number, h: number, d: number, r = 0.08) => {
	const k = [w, h, d, r].join('|');
	if (!geoCache.has(k)) geoCache.set(k, new RoundedBoxGeometry(w, h, d, 3, r));
	return geoCache.get(k)!;
};

export type Pose = {
	walk?: number; // phase in radians
	walkAmt?: number; // 0..1 swing amount
	armsUp?: number; // 0..1 panic arms
	fly?: number; // 0..1 superman pose
	sit?: number; // 0..1
	wave?: number; // 0..1 right arm wave
	headYaw?: number;
	headPitch?: number;
	lean?: number; // forward lean (radians)
	time?: number; // seconds, for idle motion
	sixSeven?: number; // 0..1 the "6 7" hands (palms up, alternating)
	flex?: number; // 0..1 double biceps flex
	cover?: number; // 0..1 hands over face (crying)
	point?: number; // 0..1 right arm points forward
	jump?: number; // height offset
	turn?: number; // body yaw offset
};

export type Look = {
	head: string;
	torso: string;
	arms: string;
	legs: string;
	face: FaceKind;
	shirt?: 'req' | 'plain' | 'stripe' | 'heart' | 'suit' | 'abs' | 'lia' | 'yf' | 'kid';
	shirtColor?: string;
	hat?: 'cap' | 'hood' | 'bacon' | 'tophat' | 'veil' | 'backcap' | 'duckhood' | 'none';
	hatColor?: string;
	hair?: 'long' | 'pigtails';
	hairColor?: string;
	bow?: string;
	skirt?: string;
	buff?: boolean;
	wings?: boolean;
	glow?: number;
};

const mat = (color: string, extra: Partial<THREE.MeshStandardMaterialParameters> = {}) => (
	<meshStandardMaterial color={color} roughness={0.55} metalness={0.02} {...extra} />
);

export const Avatar: React.FC<{
	look: Look;
	pose?: Pose;
	position?: [number, number, number];
	rotationY?: number;
	scale?: number;
}> = ({look, pose = {}, position = [0, 0, 0], rotationY = 0, scale = 1}) => {
	const {walk = 0, walkAmt = 0, armsUp = 0, fly = 0, sit = 0, wave = 0, headYaw = 0, headPitch = 0, lean = 0, time = 0} = pose;
	const {sixSeven = 0, flex = 0, cover = 0, point = 0, jump = 0, turn = 0} = pose;
	const swing = Math.sin(walk) * 0.9 * walkAmt;
	const idle = Math.sin(time * 1.6) * 0.04 * (1 - walkAmt);
	const bob = Math.abs(Math.cos(walk)) * 0.12 * walkAmt;

	// arms
	let armL = -swing + idle;
	let armR = swing - idle;
	let armLz = 0;
	let armRz = 0;
	if (armsUp > 0) {
		const wig = Math.sin(time * 18) * 0.25;
		armL = THREE.MathUtils.lerp(armL, -Math.PI * 0.92 + wig, armsUp);
		armR = THREE.MathUtils.lerp(armR, -Math.PI * 0.92 - wig, armsUp);
	}
	if (fly > 0) {
		armL = THREE.MathUtils.lerp(armL, -Math.PI * 0.95, fly);
		armR = THREE.MathUtils.lerp(armR, -0.2, fly);
		armRz = THREE.MathUtils.lerp(0, -0.9, fly);
	}
	if (wave > 0) {
		armR = THREE.MathUtils.lerp(armR, -Math.PI * 0.85, wave);
		armRz = THREE.MathUtils.lerp(armRz, -0.3 + Math.sin(time * 10) * 0.35, wave);
	}
	if (sixSeven > 0) {
		const ph = Math.sin(time * 9);
		armL = THREE.MathUtils.lerp(armL, -1.35 + ph * 0.45, sixSeven);
		armR = THREE.MathUtils.lerp(armR, -1.35 - ph * 0.45, sixSeven);
	}
	if (flex > 0) {
		armL = THREE.MathUtils.lerp(armL, -0.25, flex);
		armR = THREE.MathUtils.lerp(armR, -0.25, flex);
		armLz = THREE.MathUtils.lerp(armLz, 2.2 + Math.sin(time * 6) * 0.08, flex);
		armRz = THREE.MathUtils.lerp(armRz, -2.2 - Math.sin(time * 6) * 0.08, flex);
	}
	if (cover > 0) {
		const sob = Math.sin(time * 14) * 0.06;
		armL = THREE.MathUtils.lerp(armL, -2.55 + sob, cover);
		armR = THREE.MathUtils.lerp(armR, -2.55 - sob, cover);
		armLz = THREE.MathUtils.lerp(armLz, -0.38, cover);
		armRz = THREE.MathUtils.lerp(armRz, 0.38, cover);
	}
	if (point > 0) {
		armR = THREE.MathUtils.lerp(armR, -1.55, point);
	}
	let legL = swing;
	let legR = -swing;
	if (sit > 0) {
		legL = THREE.MathUtils.lerp(legL, -Math.PI / 2, sit);
		legR = THREE.MathUtils.lerp(legR, -Math.PI / 2, sit);
	}
	if (fly > 0) {
		legL = THREE.MathUtils.lerp(legL, 0.25, fly);
		legR = THREE.MathUtils.lerp(legR, 0.05, fly);
	}

	const face = useMemo(() => faceTexture(look.face), [look.face]);
	const shirt = useMemo(
		() => (look.shirt && look.shirt !== 'plain' ? shirtTexture(look.shirt, look.shirtColor) : null),
		[look.shirt, look.shirtColor],
	);
	const emissive = look.glow ? {emissive: new THREE.Color('#ffffff'), emissiveIntensity: look.glow} : {};
	const flap = Math.sin(time * 9) * 0.45;
	const B = look.buff;
	const tw = B ? 2.7 : 2; // torso width
	const td = B ? 1.35 : 1;
	const aw = B ? 1.3 : 1; // arm thickness
	const sx = B ? 2.0 : 1.5; // shoulder x
	const sy = B ? 4.05 : 3.85;
	const ty = B ? 3.1 : 3;
	const th = B ? 2.2 : 2;
	const headY = B ? 4.2 : 4.0;

	return (
		<group position={position} rotation={[0, rotationY + turn, 0]} scale={scale}>
			<group position={[0, bob - sit * 1.0 + jump, 0]} rotation={[lean + fly * 1.35, 0, 0]}>
				{/* torso */}
				<mesh position={[0, ty, 0]} geometry={rbox(tw, th, td, 0.07)} castShadow receiveShadow>
					{mat(look.torso, emissive)}
				</mesh>
				{look.skirt ? (
					<mesh position={[0, 1.55, 0]} scale={[1.45, 1, 0.78]} castShadow>
						<cylinderGeometry args={[1.0, 1.35, 1.1, 4, 1, false, Math.PI / 4]} />
						{mat(look.skirt)}
					</mesh>
				) : null}
				{shirt ? (
					<mesh position={[0, ty, td / 2 + 0.005]}>
						<planeGeometry args={[tw, th]} />
						<meshStandardMaterial map={shirt} transparent roughness={0.6} polygonOffset polygonOffsetFactor={-1} />
					</mesh>
				) : null}
				{/* head */}
				<group position={[0, headY, 0]} rotation={[headPitch, headYaw, 0]}>
					<mesh position={[0, 0.62, 0]} geometry={rbox(1.25, 1.22, 1.22, 0.32)} castShadow>
						{mat(look.head, emissive)}
					</mesh>
					<mesh position={[0, 0.62, 0.615]}>
						<planeGeometry args={[1.1, 1.1]} />
						<meshStandardMaterial
							map={face}
							transparent
							roughness={0.5}
							polygonOffset
							polygonOffsetFactor={-2}
							{...(look.face === 'kli' ? {emissive: new THREE.Color('#ffffff'), emissiveMap: face, emissiveIntensity: 0.6} : {})}
						/>
					</mesh>
					<Hat look={look} />
					<Hair look={look} />
				</group>
				{/* arms */}
				<group position={[-sx, sy, 0]} rotation={[armL, 0, -armLz + 0.02]}>
					<mesh position={[0, -0.85, 0]} geometry={rbox(aw, B ? 2.1 : 2, aw, 0.07)} castShadow>
						{mat(look.arms, emissive)}
					</mesh>
				</group>
				<group position={[sx, sy, 0]} rotation={[armR, 0, armRz - 0.02]}>
					<mesh position={[0, -0.85, 0]} geometry={rbox(aw, B ? 2.1 : 2, aw, 0.07)} castShadow>
						{mat(look.arms, emissive)}
					</mesh>
				</group>
				{/* legs */}
				<group position={[-0.5, 2, 0]} rotation={[legL, 0, 0]}>
					<mesh position={[0, -1, 0]} geometry={rbox(0.99, 2, 1, 0.07)} castShadow>
						{mat(look.legs, emissive)}
					</mesh>
				</group>
				<group position={[0.5, 2, 0]} rotation={[legR, 0, 0]}>
					<mesh position={[0, -1, 0]} geometry={rbox(0.99, 2, 1, 0.07)} castShadow>
						{mat(look.legs, emissive)}
					</mesh>
				</group>
				{look.wings ? (
					<group position={[0, 3.4, -0.55]}>
						{[-1, 1].map((s) => (
							<group key={s} rotation={[0, s * (0.55 + flap), s * 0.25]}>
								{[
									[2.6, 0.55, 0.9, 0.45],
									[2.2, 0.5, 0.35, 0.15],
									[1.7, 0.45, -0.15, -0.15],
									[1.2, 0.4, -0.6, -0.45],
								].map(([len, h, y, rz], n) => (
									<mesh key={n} position={[s * (0.3 + len / 2), y, -n * 0.04]} rotation={[0, 0, s * rz]} geometry={rbox(len, h, 0.12, 0.05)} castShadow>
										<meshStandardMaterial color="#ffffff" emissive="#ffd9f2" emissiveIntensity={0.35} roughness={0.5} />
									</mesh>
								))}
							</group>
						))}
					</group>
				) : null}
			</group>
		</group>
	);
};

const Hat: React.FC<{look: Look}> = ({look}) => {
	const c = look.hatColor ?? '#d32f2f';
	switch (look.hat) {
		case 'cap':
			return (
				<group position={[0, 1.18, 0]}>
					<mesh geometry={rbox(1.36, 0.42, 1.34, 0.18)} castShadow>
						{mat(c)}
					</mesh>
					<mesh position={[0, -0.14, -0.86]} geometry={rbox(1.0, 0.1, 0.6, 0.04)} castShadow>
						{mat(c)}
					</mesh>
					<mesh position={[0, 0.0, 0.68]}>
						<planeGeometry args={[0.5, 0.26]} />
						<meshStandardMaterial color="#ffffff" />
					</mesh>
				</group>
			);
		case 'hood':
			return (
				<group>
					<mesh position={[0, 0.82, -0.08]} geometry={rbox(1.42, 1.0, 1.32, 0.34)} castShadow>
						{mat(c)}
					</mesh>
				</group>
			);
		case 'bacon':
			return (
				<mesh position={[0, 1.0, -0.05]} geometry={rbox(1.38, 0.62, 1.36, 0.2)} castShadow>
					{mat(c)}
				</mesh>
			);
		case 'tophat':
			return (
				<group position={[0, 1.25, 0]}>
					<mesh position={[0, 0.0, 0]}>
						<cylinderGeometry args={[0.95, 0.95, 0.08, 24]} />
						{mat('#111')}
					</mesh>
					<mesh position={[0, 0.5, 0]} castShadow>
						<cylinderGeometry args={[0.55, 0.55, 1.0, 24]} />
						{mat('#111')}
					</mesh>
				</group>
			);
		case 'backcap':
			return (
				<group position={[0, 1.18, 0]}>
					<mesh geometry={rbox(1.36, 0.42, 1.34, 0.18)} castShadow>
						{mat(c)}
					</mesh>
					<mesh position={[0, -0.14, -0.86]} geometry={rbox(1.0, 0.1, 0.6, 0.04)} castShadow>
						{mat(c)}
					</mesh>
				</group>
			);
		case 'duckhood':
			return (
				<group>
					<mesh position={[0, 0.84, -0.1]} geometry={rbox(1.46, 1.06, 1.34, 0.36)} castShadow>
						{mat(c)}
					</mesh>
					{/* little white buttons + ear tufts like the skin */}
					{[-0.42, 0.42].map((x) => (
						<mesh key={x} position={[x, 1.42, 0.3]} geometry={rbox(0.22, 0.22, 0.22, 0.05)}>
							<meshStandardMaterial color="#f0e9e7" />
						</mesh>
					))}
				</group>
			);
		case 'veil':
			return (
				<group>
					<mesh position={[0, 1.33, 0]}>
						<torusGeometry args={[0.5, 0.08, 8, 24]} />
						<meshStandardMaterial color="#ffd54a" metalness={0.8} roughness={0.25} />
					</mesh>
					<mesh position={[0, 0.5, -0.75]} rotation={[0.12, 0, 0]}>
						<boxGeometry args={[1.5, 1.9, 0.04]} />
						<meshStandardMaterial color="#ffffff" transparent opacity={0.55} roughness={0.3} />
					</mesh>
				</group>
			);
		default:
			return null;
	}
};

const Hair: React.FC<{look: Look}> = ({look}) => {
	if (!look.hair) return null;
	const c = look.hairColor ?? '#5a3825';
	const m = <meshStandardMaterial color={c} roughness={0.7} />;
	return (
		<group>
			{/* cap of hair + bangs */}
			<mesh position={[0, 1.02, -0.05]} geometry={rbox(1.42, 0.5, 1.38, 0.22)} castShadow>
				{m}
			</mesh>
			<mesh position={[0.25, 0.92, 0.6]} rotation={[0, 0, -0.25]} geometry={rbox(0.8, 0.28, 0.16, 0.06)} castShadow>
				{m}
			</mesh>
			{look.hair === 'long' ? (
				<>
					<mesh position={[0, 0.2, -0.55]} geometry={rbox(1.42, 1.9, 0.4, 0.15)} castShadow>
						{m}
					</mesh>
					{[-1, 1].map((s) => (
						<mesh key={s} position={[s * 0.66, 0.35, -0.1]} geometry={rbox(0.18, 1.5, 0.9, 0.06)} castShadow>
							{m}
						</mesh>
					))}
				</>
			) : (
				[-1, 1].map((s) => (
					<mesh key={s} position={[s * 0.95, 0.3, -0.2]} rotation={[0, 0, s * 0.2]} geometry={rbox(0.45, 1.4, 0.45, 0.2)} castShadow>
						{m}
					</mesh>
				))
			)}
			{look.bow ? (
				<group position={[0.45, 1.32, 0.1]} rotation={[0, 0, -0.3]}>
					{[-1, 1].map((s) => (
						<mesh key={s} position={[s * 0.22, 0, 0]} rotation={[0, 0, Math.PI / 4]} geometry={rbox(0.32, 0.32, 0.14, 0.05)}>
							<meshStandardMaterial color={look.bow} />
						</mesh>
					))}
					<mesh geometry={rbox(0.14, 0.14, 0.18, 0.04)}>
						<meshStandardMaterial color={look.bow} />
					</mesh>
				</group>
			) : null}
		</group>
	);
};

// ---------------------------------------------------------------- looks
export const REQ_LOOK: Look = {
	head: '#f5cd30',
	torso: '#1f2a44',
	arms: '#1f2a44',
	legs: '#3a3f47',
	face: 'smile',
	shirt: 'req',
	hat: 'cap',
	hatColor: '#d62828',
};

export const KLI_LOOK: Look = {
	head: '#0b0b0d',
	torso: '#0b0b0d',
	arms: '#0b0b0d',
	legs: '#0b0b0d',
	face: 'kli',
	hat: 'hood',
	hatColor: '#0e0e10',
	wings: true,
};

export const LIA_LOOK: Look = {
	head: '#ffdcc2',
	torso: '#ff8fc8',
	arms: '#ffdcc2',
	legs: '#ffdcc2',
	face: 'lia',
	shirt: 'lia',
	skirt: '#ffffff',
	hair: 'long',
	hairColor: '#6b3e26',
	bow: '#ff4fa3',
};

export const KLI_MM2: Look = {...KLI_LOOK, wings: false};

// kli before Blender: a broke default noob
export const NOOB_KLI: Look = {
	head: '#f5cd30',
	torso: '#1e6fd9',
	arms: '#f5cd30',
	legs: '#4caf50',
	face: 'smile',
};

// kli after Blender: the deep-voiced legend, gold hood once he's rich
export const KLI_DEEP: Look = {...KLI_MM2, buff: true};
export const KLI_RICH: Look = {...KLI_MM2, buff: true, hatColor: '#d9a520', shirt: 'suit', shirtColor: '#d9a520'};

export const MYNINN_LOOK: Look = {
	head: '#ffe0bd',
	torso: '#14a89c',
	arms: '#14a89c',
	legs: '#263238',
	face: 'grin',
	shirt: 'stripe',
	shirtColor: '#e0fffb',
	hat: 'backcap',
	hatColor: '#111111',
};

export const MIKEY_LOOK: Look = {
	head: '#eac39b',
	torso: '#2f6fe0',
	arms: '#2f6fe0',
	legs: '#263238',
	face: 'grin',
	shirt: 'stripe',
	shirtColor: '#ffffff',
	hat: 'bacon',
	hatColor: '#4e342e',
};

export const ADE_LOOK: Look = {
	head: '#c58c5c',
	torso: '#2fbf71',
	arms: '#2fbf71',
	legs: '#1b1b1f',
	face: 'smile',
	shirt: 'heart',
	shirtColor: '#ffeb3b',
	hat: 'cap',
	hatColor: '#111111',
};

export const YF_LOOK: Look = {
	head: '#f5cd30',
	torso: '#5b5f66',
	arms: '#5b5f66',
	legs: '#2b2d31',
	face: 'angry',
	shirt: 'yf',
	hat: 'backcap',
	hatColor: '#c62828',
};

// BoompjeJunior: purple duck hoodie skin, but make it muscles
export const BOOMP_LOOK: Look = {
	head: '#f3dc9d',
	torso: '#7f539e',
	arms: '#6d4587',
	legs: '#b55ac0',
	face: 'duck',
	shirt: 'abs',
	shirtColor: '#5c3a78',
	hat: 'duckhood',
	hatColor: '#593a6e',
	buff: true,
};

export const kidLook = (i: number): Look => {
	const r = (k: number) => Math.abs(Math.sin(i * 57.3 + k * 11.1) * 1000) % 1;
	const girl = r(1) > 0.5;
	return {
		head: r(2) > 0.5 ? '#ffdcc2' : '#f3dc9d',
		torso: ['#ff8fc8', '#7f539e', '#b55ac0', '#ff6fb5', '#9b6bd1'][Math.floor(r(3) * 5)],
		arms: r(4) > 0.5 ? '#ffdcc2' : '#6d4587',
		legs: ['#ffffff', '#b55ac0', '#593a6e'][Math.floor(r(5) * 3)],
		face: r(6) > 0.5 ? 'duck' : 'happy',
		shirt: 'kid',
		hair: girl ? (r(7) > 0.5 ? 'long' : 'pigtails') : undefined,
		hairColor: r(8) > 0.5 ? '#6b3e26' : '#593a6e',
		hat: girl ? undefined : 'duckhood',
		hatColor: '#593a6e',
	};
};

const SKIN = ['#f5cd30', '#eac39b', '#c58c5c', '#8d5a3a', '#ffe0bd', '#f5cd30'];
const COLORS = ['#e53935', '#43a047', '#1e88e5', '#fdd835', '#8e24aa', '#fb8c00', '#00acc1', '#f06292', '#6d4c41', '#3949ab', '#ffffff', '#212121'];

export const NPC_NAMES = ['Emii5287', 'kaiib', 'HachiMC', 'GamingSquirrel39', 'lewlone', 'KirbyUPUP', 'BoompjeJunior', 'bacon_hair2012', 'xXnoobslayerXx', 'pet_trader99', 'Lilyy_bloom', 'Toast_YT'];

export const npcLook = (i: number): Look => {
	const r = (k: number) => Math.abs(Math.sin(i * 91.7 + k * 13.3) * 1000) % 1;
	const pick = <T,>(arr: T[], k: number) => arr[Math.floor(r(k) * arr.length)];
	const hats: Look['hat'][] = ['bacon', 'none', 'cap', 'bacon', 'tophat', 'none'];
	return {
		head: pick(SKIN, 1),
		torso: pick(COLORS, 2),
		arms: r(7) > 0.5 ? pick(SKIN, 1) : pick(COLORS, 2),
		legs: pick(['#263238', '#1565c0', '#4e342e', '#37474f', '#2e7d32'], 3),
		face: pick<FaceKind>(['smile', 'grin', 'smile', 'happy'], 4),
		shirt: pick<Look['shirt']>(['plain', 'stripe', 'heart', 'plain'], 5),
		shirtColor: pick(['#ffffff', '#111111', '#ffeb3b'], 8),
		hat: pick(hats, 6),
		hatColor: pick(['#5d4037', '#3e2723', '#d32f2f', '#1976d2', '#fbc02d'], 9),
	};
};
