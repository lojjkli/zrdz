import React, {useMemo} from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';
import {Avatar, kidLook, Look, Pose, rbox} from '../three/Avatar';
import {Cam, ease, lerp3, range, V3} from '../three/cam';
import {FaceKind} from '../three/textures';
import {Machine} from '../three/Props';
import {Env, Stage} from '../three/World';
import {Windmill} from '../three/MM2World';
import {baseplateTexture, Bread, DefaultCube, Pigeon, TalkingDonut} from '../three/KliProps';
import {BEATS, beatAt, BIGS, FLASHES, FPS, Span, SPEAKER_TAG, talking} from '../timeline';
import {Billboards, BB} from '../ui/Billboards';
import {DOC_FONT, UI_FONT} from '../ui/HUD';
import {BigText, GameUI} from '../ui/MM2';
import {Fade, Flash} from '../ui/KliUI';
import {Grain, Letterbox, Vignette} from './Doc';
import {face, withShake} from './shots';

export const Y = 0.05;
const std = (color: string, extra: Record<string, unknown> = {}) => <meshStandardMaterial color={color} roughness={0.6} {...extra} />;

// ---------------------------------------------------------------- time helpers
/** eased path through [time, position] keys */
export const path = (t: number, keys: [number, V3][], dur = 0.8): V3 => {
	let p = keys[0][1];
	for (let i = 1; i < keys.length; i++) {
		const [at, q] = keys[i];
		if (t >= at) p = q;
		else if (t > at - dur) return lerp3(p, q, ease(range(t, at - dur, at)));
	}
	return p;
};
/** the last value whose time has passed */
export const pick = <X,>(t: number, keys: [number, X][]): X => {
	let v = keys[0][1];
	for (const [at, x] of keys) if (t >= at) v = x;
	return v;
};
export const during = (t: number, a: number, b: number) => t >= a && t < b;

// ---------------------------------------------------------------- set pieces
export const Grass: React.FC<{color?: string}> = ({color = '#5aa83e'}) => (
	<mesh position={[0, -0.5, 0]} receiveShadow>
		<boxGeometry args={[600, 1, 600]} />
		<meshStandardMaterial map={baseplateTexture('psgrass', color, '#4f9a36', 140)} roughness={0.9} />
	</mesh>
);

export const Floor: React.FC<{color: string; size?: number}> = ({color, size = 120}) => (
	<mesh position={[0, -0.5, 0]} receiveShadow>
		<boxGeometry args={[size, 1, size]} />
		<meshStandardMaterial color={color} roughness={0.5} />
	</mesh>
);

export const Chair: React.FC<{position: V3; rotationY?: number}> = ({position, rotationY = 0}) => (
	<group position={position} rotation={[0, rotationY, 0]}>
		<mesh position={[0, 0.5, 0]} rotation={[-0.15, 0, 0]}>
			<boxGeometry args={[1.8, 0.12, 2.2]} />
			<meshStandardMaterial color="#4fd2ff" />
		</mesh>
		<mesh position={[0, 1.2, -1.0]} rotation={[-0.5, 0, 0]}>
			<boxGeometry args={[1.8, 1.6, 0.12]} />
			<meshStandardMaterial color="#4fd2ff" />
		</mesh>
	</group>
);

export const Juice: React.FC<{position: V3}> = ({position}) => (
	<group position={position}>
		<mesh position={[0, 0.3, 0]}>
			<cylinderGeometry args={[0.2, 0.15, 0.6, 12]} />
			<meshStandardMaterial color="#ffb347" transparent opacity={0.85} />
		</mesh>
		<mesh position={[0.08, 0.7, 0]} rotation={[0, 0, -0.3]}>
			<cylinderGeometry args={[0.03, 0.03, 0.6, 6]} />
			<meshStandardMaterial color="#ff4fa0" />
		</mesh>
	</group>
);

/** googly eyes, centred at the origin, looking +z */
export const Eyes: React.FC<{gap?: number; size?: number; t?: number}> = ({gap = 0.25, size = 0.12, t = 0}) => (
	<>
		{[-1, 1].map((k) => (
			<group key={k} position={[k * gap, 0, 0]}>
				<mesh scale={[1, 1, 0.5]}>
					<sphereGeometry args={[size, 12, 10]} />
					<meshStandardMaterial color="#fff" roughness={0.2} />
				</mesh>
				<mesh position={[Math.sin(t * 3 + k) * size * 0.25, -size * 0.2, size * 0.45]}>
					<sphereGeometry args={[size * 0.5, 10, 8]} />
					<meshBasicMaterial color="#111" />
				</mesh>
			</group>
		))}
	</>
);

export const Heart: React.FC<{position: V3; s?: number}> = ({position, s = 1}) => (
	<group position={position} scale={s}>
		{[-1, 1].map((k) => (
			<mesh key={k} position={[k * 0.28, 0.15, 0]}>
				<sphereGeometry args={[0.36, 12, 10]} />
				<meshBasicMaterial color="#ff3f7f" />
			</mesh>
		))}
		<mesh position={[0, -0.18, 0]} rotation={[0, 0, Math.PI / 4]}>
			<boxGeometry args={[0.6, 0.6, 0.5]} />
			<meshBasicMaterial color="#ff3f7f" />
		</mesh>
	</group>
);

/** hearts floating up from a point while k > 0 */
export const HeartPuff: React.FC<{at: V3; t: number; k: number}> = ({at, t, k}) =>
	k <= 0 ? null : (
		<>
			{[0, 1, 2, 3, 4].map((i) => {
				const ph = (t * 0.6 + i / 5) % 1;
				return <Heart key={i} position={[at[0] + Math.sin(i * 2.3) * 1.2, at[1] + ph * 3, at[2] + Math.cos(i * 1.7) * 0.6]} s={0.5 * k * (1 - ph * 0.6)} />;
			})}
		</>
	);

// ---------------------------------------------------------------- creatures
/** The hamster that ran the Lucky Spin. Faces +z, feet at y=0. */
export const Hamster: React.FC<{position: V3; rotationY?: number; t: number; scale?: number; run?: number; shades?: boolean; tired?: boolean; jump?: number; hat?: boolean}> = ({position, rotationY = 0, t, scale = 1, run = 0, shades, tired, jump = 0, hat}) => {
	const bob = Math.abs(Math.sin(t * 22)) * 0.12 * run + jump;
	return (
		<group position={[position[0], position[1] + bob, position[2]]} rotation={[0, rotationY, 0]} scale={scale}>
			<mesh position={[0, 0.75, 0]} geometry={rbox(1.5, 1.3, 1.7, 0.55)} castShadow>
				{std('#e8a35a')}
			</mesh>
			<mesh position={[0, 0.6, 0.62]} geometry={rbox(1.0, 0.8, 0.5, 0.3)}>
				{std('#fff3e2')}
			</mesh>
			{[-1, 1].map((s) => (
				<group key={s}>
					<mesh position={[s * 0.48, 1.45, 0.1]}>
						<sphereGeometry args={[0.24, 12, 10]} />
						{std('#d48a46')}
					</mesh>
					<mesh position={[s * 0.3, tired ? 1.0 : 1.05, 0.86]} scale={[1, tired ? 0.35 : 1, 1]}>
						<sphereGeometry args={[0.11, 10, 8]} />
						{std('#111', {roughness: 0.2})}
					</mesh>
					<mesh position={[s * 0.5, 0.82, 0.78]} scale={[1, 0.8, 0.5]}>
						<sphereGeometry args={[0.2, 10, 8]} />
						{std('#ffcf9a')}
					</mesh>
					<mesh position={[s * 0.4, 0.12 + Math.sin(t * 22 + s) * 0.08 * run, 0.35]}>
						<boxGeometry args={[0.3, 0.24, 0.4]} />
						{std('#ffb3c1')}
					</mesh>
				</group>
			))}
			<mesh position={[0, 0.9, 0.9]}>
				<sphereGeometry args={[0.08, 8, 6]} />
				{std('#ff6b8b')}
			</mesh>
			{shades ? (
				<group position={[0, 1.07, 0.92]}>
					{[-1, 1].map((s) => (
						<mesh key={s} position={[s * 0.3, 0, 0]}>
							<boxGeometry args={[0.42, 0.24, 0.05]} />
							<meshStandardMaterial color="#111" roughness={0.1} metalness={0.6} />
						</mesh>
					))}
				</group>
			) : null}
			{hat ? (
				<group position={[0, 1.55, 0]}>
					<mesh>
						<cylinderGeometry args={[0.55, 0.55, 0.06, 16]} />
						{std('#111')}
					</mesh>
					<mesh position={[0, 0.35, 0]}>
						<cylinderGeometry args={[0.35, 0.35, 0.7, 16]} />
						{std('#111')}
					</mesh>
				</group>
			) : null}
		</group>
	);
};

/** Lia's giant windmill with a face. */
export const GiantMill: React.FC<{p: V3; s: number; yaw: number; spin: number; fall?: number; eyes?: number; mood?: 'angry' | 'love' | 'happy' | 'sad'}> = ({p, s, yaw, spin, fall = 0, eyes = 1, mood = 'happy'}) => {
	const eyeCol = mood === 'angry' ? '#ff2a1a' : mood === 'sad' ? '#8fd0ff' : '#ffffff';
	return (
		<group position={p} rotation={[0, yaw, 0]}>
			<group rotation={[0, 0, -fall * Math.PI * 0.5]} scale={s}>
				<Windmill position={[0, 0, 0]} t={spin / 1.4} s={1} />
				{eyes > 0
					? [-1, 1].map((k) => (
							<group key={k} position={[k * 1.25, 6.6, 3.8]} rotation={[0, 0, mood === 'angry' ? k * 0.35 : mood === 'sad' ? -k * 0.3 : 0]}>
								<mesh scale={[1, mood === 'happy' ? 0.35 : 1, 1]}>
									<boxGeometry args={[1.3, mood === 'angry' || mood === 'sad' ? 0.6 : 1.1, 0.2]} />
									<meshStandardMaterial color={eyeCol} emissive={eyeCol} emissiveIntensity={1.6 * eyes} />
								</mesh>
								{mood === 'love' ? (
									<mesh position={[0, 0, 0.12]}>
										<boxGeometry args={[0.6, 0.6, 0.05]} />
										<meshBasicMaterial color="#ff4f9a" />
									</mesh>
								) : null}
							</group>
					  ))
					: null}
				{mood !== 'angry' && eyes > 0
					? [-1, 1].map((k) => (
							<mesh key={'b' + k} position={[k * 2.3, 5.4, 3.75]}>
								<circleGeometry args={[0.55, 16]} />
								<meshBasicMaterial color="#ff8fb8" transparent opacity={0.85} />
							</mesh>
					  ))
					: null}
			</group>
		</group>
	);
};

/** a bagel with eyelashes (she is very fancy) */
export const Bagel: React.FC<{position: V3; yaw?: number; t: number; talk?: boolean; scale?: number; open?: number}> = ({position, yaw = 0, t, talk, scale = 1, open = 0}) => {
	const m = talk ? 0.25 + Math.abs(Math.sin(t * 14)) * 0.75 : 0.15;
	return (
		<group position={position} rotation={[0, yaw, 0]} scale={scale}>
			<group position={[0, 1.45, 0]}>
				{[-1, 1].map((k) => (
					<group key={k} position={[k * open * 1.6, open * 0.6, 0]} rotation={[0, 0, k * open * 0.6]}>
						<mesh castShadow rotation={[0, 0, k > 0 ? 0 : Math.PI]}>
							<torusGeometry args={[1, 0.5, 18, 36, open > 0 ? Math.PI : Math.PI * 2]} />
							<meshStandardMaterial color="#d8a25a" roughness={0.8} />
						</mesh>
					</group>
				))}
				{open <= 0 ? (
					<>
						{new Array(18).fill(0).map((_, i) => {
							const a = (i / 18) * Math.PI * 2;
							return (
								<mesh key={i} position={[Math.cos(a) * (1 + Math.sin(i * 7) * 0.2), Math.sin(a) * (1 + Math.cos(i * 5) * 0.2), 0.5]} rotation={[0, 0, a]}>
									<sphereGeometry args={[0.07, 6, 4]} />
									<meshStandardMaterial color="#fff6dc" />
								</mesh>
							);
						})}
						<group position={[0, 0.85, 0.5]}>
							<Eyes gap={0.45} size={0.2} t={t} />
							{[-1, 1].map((k) => (
								<mesh key={k} position={[k * 0.6, 0.18, 0.05]} rotation={[0, 0, k * 0.5]}>
									<boxGeometry args={[0.18, 0.04, 0.04]} />
									<meshBasicMaterial color="#111" />
								</mesh>
							))}
						</group>
						<mesh position={[0, -0.9, 0.52]} scale={[1, m, 1]}>
							<boxGeometry args={[0.5, 0.3, 0.05]} />
							<meshBasicMaterial color="#c2185b" />
						</mesh>
					</>
				) : null}
			</group>
		</group>
	);
};

/** the default cube, now with a face (and sometimes a judge wig) */
export const CubeGuy: React.FC<{position: V3; yaw?: number; t: number; scale?: number; talk?: boolean; wig?: boolean}> = ({position, yaw = 0, t, scale = 1, talk, wig}) => (
	<group position={position} rotation={[0, yaw, 0]} scale={scale}>
		<DefaultCube position={[0, 1, 0]} scale={1} selected={false} />
		<group position={[0, 1.35, 1.02]}>
			<Eyes gap={0.35} size={0.16} t={t} />
		</group>
		<mesh position={[0, 0.6, 1.02]} scale={[1, talk ? 0.3 + Math.abs(Math.sin(t * 14)) : 0.3, 1]}>
			<boxGeometry args={[0.5, 0.25, 0.04]} />
			<meshBasicMaterial color="#222" />
		</mesh>
		{wig
			? [-1, 0, 1].map((k) => (
					<mesh key={k} position={[k * 0.75, 2.15, 0]}>
						<sphereGeometry args={[0.45, 12, 10]} />
						<meshStandardMaterial color="#f4f1ea" roughness={0.9} />
					</mesh>
			  ))
			: null}
	</group>
);

export const BreadGuy: React.FC<{position: V3; yaw?: number; t: number; scale?: number}> = ({position, yaw = 0, t, scale = 1}) => (
	<group position={position} rotation={[0, yaw, 0]} scale={scale}>
		<Bread position={[0, 0.3, 0]} />
		<group position={[0, 0.45, 0.32]}>
			<Eyes gap={0.18} size={0.09} t={t * 0.3} />
		</group>
	</group>
);

const KIDS: V3[] = (() => {
	const out: V3[] = [];
	for (let r = 0; r < 5; r++) for (let c = 0; c < 10; c++) out.push([(c - 4.5) * 1.9 + Math.sin(r * 7 + c) * 0.3, 0, r * 2.0]);
	return out;
})();
export const Kids: React.FC<{p: V3; t: number; yaw?: number; jump?: number; armsUp?: number}> = ({p, t, yaw = 0, jump = 0, armsUp = 0}) => {
	const looks = useMemo(() => KIDS.map((_, i) => kidLook(i + 3)), []);
	return (
		<group position={p}>
			{KIDS.map((k, i) => (
				<Avatar key={i} look={looks[i]} position={[k[0], Y + Math.abs(Math.sin(t * 8 + i)) * jump, k[2]]} scale={0.45} rotationY={yaw} pose={{time: t + i * 0.37, armsUp}} />
			))}
		</group>
	);
};

// ---------------------------------------------------------------- actors + scenes
export type Kind = 'avatar' | 'machine' | 'pigeon' | 'hamster' | 'donut' | 'mill' | 'cube' | 'bread' | 'bagel' | 'kids';

export type Actor = {
	id: string;
	kind: Kind;
	look?: Look;
	/** nametag; null hides it */
	name?: string | null;
	p: V3 | ((t: number) => V3);
	yaw?: number | ((t: number) => number);
	s?: number;
	face?: (t: number) => FaceKind;
	pose?: (t: number) => Pose;
	/** extra props for the creature */
	x?: (t: number) => Record<string, unknown>;
	show?: (t: number) => boolean;
	/** close-up override: [target height, distance] (before scale) */
	cu?: [number, number];
	/** which side the close-up camera sits on: 1 or -1 */
	side?: number;
};

export type SceneDef = {
	env: Env;
	/** actors face this point unless told otherwise */
	front: V3;
	wides: ((t: number) => Cam)[];
	shots?: Record<string, (t: number, k: number) => Cam>;
	cast: Actor[];
	set?: (t: number) => React.ReactNode;
	over?: (t: number) => React.ReactNode;
	shake?: (t: number) => number;
};

// [close-up target height, distance, nametag height]
const SIZE: Record<Kind, [number, number, number]> = {
	avatar: [4.15, 7.2, 5.7],
	machine: [9.5, 24, 18.2],
	pigeon: [0.9, 4.2, 1.7],
	hamster: [1.0, 5.4, 2.1],
	donut: [1.5, 6.4, 3.3],
	mill: [6.0, 23, 13.5],
	cube: [1.2, 6, 2.8],
	bread: [0.5, 3.2, 1.3],
	bagel: [1.5, 6.4, 3.3],
	kids: [2, 12, 3],
};

const posOf = (a: Actor, t: number): V3 => (typeof a.p === 'function' ? a.p(t) : a.p);
const yawOf = (a: Actor, t: number, front: V3): number =>
	a.yaw === undefined ? face(posOf(a, t), front) : typeof a.yaw === 'function' ? a.yaw(t) : a.yaw;

export const closeUp = (a: Actor, t: number, front: V3, side = 1): Cam => {
	const p = posOf(a, t);
	const s = a.s ?? 1;
	const [h, d] = a.cu ?? SIZE[a.kind];
	const ang = yawOf(a, t, front) + side * 0.32;
	const dist = d * s;
	return {
		pos: [p[0] + Math.sin(ang) * dist + Math.sin(t * 0.4) * 0.1 * s, p[1] + (h + 0.35) * s, p[2] + Math.cos(ang) * dist],
		target: [p[0], p[1] + h * s, p[2]],
		fov: 40,
	};
};

export const twoShot = (a: Actor, b: Actor, t: number, front: V3): Cam => {
	const pa = posOf(a, t);
	const pb = posOf(b, t);
	const mid: V3 = [(pa[0] + pb[0]) / 2, (pa[1] + pb[1]) / 2, (pa[2] + pb[2]) / 2];
	const h = (SIZE[a.kind][0] * (a.s ?? 1) + SIZE[b.kind][0] * (b.s ?? 1)) / 2;
	const sep = Math.hypot(pa[0] - pb[0], pa[2] - pb[2]);
	let dx = front[0] - mid[0];
	let dz = front[2] - mid[2];
	const n = Math.hypot(dx, dz) || 1;
	dx /= n;
	dz /= n;
	const D = sep * 1.15 + h * 1.4 + 4;
	return {pos: [mid[0] + dx * D, mid[1] + h + 1.2, mid[2] + dz * D], target: [mid[0], mid[1] + h * 0.85, mid[2]], fov: 42};
};

const ActorView: React.FC<{a: Actor; t: number; front: V3}> = ({a, t, front}) => {
	const p = posOf(a, t);
	const yaw = yawOf(a, t, front);
	const s = a.s ?? 1;
	const talk = talking(a.id, t);
	const x = a.x ? a.x(t) : {};
	switch (a.kind) {
		case 'avatar':
			return <Avatar look={{...a.look!, face: a.face ? a.face(t) : a.look!.face}} position={p} rotationY={yaw} scale={s} pose={{time: t + p[0], ...(a.pose ? a.pose(t) : {})}} />;
		case 'machine':
			return (
				<group position={p} rotation={[0, yaw, 0]} scale={s}>
					<Machine t={t} spin={(x.spin as [number, number, number]) ?? [0.4, 1.7, 3.1]} lights={1 + (talk ? Math.abs(Math.sin(t * 12)) * 0.8 : 0) + ((x.lights as number) ?? 0)} />
				</group>
			);
		case 'pigeon':
			return <Pigeon position={p} rotationY={yaw} t={t} flap={(x.flap as number) ?? 0} scale={s} />;
		case 'hamster':
			return <Hamster position={p} rotationY={yaw} t={t} scale={s} {...x} />;
		case 'donut':
			return <TalkingDonut position={p} yaw={yaw} t={t} scale={s} talk={talk} {...x} />;
		case 'bagel':
			return <Bagel position={p} yaw={yaw} t={t} scale={s} talk={talk} {...x} />;
		case 'mill':
			return <GiantMill p={p} s={s} yaw={yaw} spin={(x.spin as number) ?? t * 1.2} {...x} />;
		case 'cube':
			return <CubeGuy position={p} yaw={yaw} t={t} scale={s} talk={talk} {...x} />;
		case 'bread':
			return <BreadGuy position={p} yaw={yaw} t={t} scale={s} />;
		case 'kids':
			return <Kids p={p} t={t} yaw={yaw} {...x} />;
	}
};

const isWide = (shot: string | undefined, speaker: string | undefined, def: SceneDef) =>
	shot ? shot.startsWith('wide') : !speaker || !def.cast.some((a) => a.id === speaker && a.kind !== 'kids');

const camFor = (def: SceneDef, scene: string, t: number): Cam => {
	const b = beatAt(t);
	const visible = def.cast.filter((a) => !a.show || a.show(t));
	if (!b || b.scene !== scene) return def.wides[0](t);
	const k = range(t, b.from, b.to);
	const shot = b.shot ?? (!isWide(undefined, b.speaker, def) && visible.some((a) => a.id === b.speaker) ? b.speaker! : 'wide');
	if (def.shots?.[shot]) return def.shots[shot](t, k);
	if (shot.startsWith('wide')) {
		const fixed = shot.length > 4 ? Number(shot.slice(4)) - 1 : null;
		const i = fixed ?? BEATS.filter((x) => x.scene === scene && x.n < b.n && isWide(x.shot, x.speaker, def) && x.shot === undefined).length;
		return def.wides[i % def.wides.length](t);
	}
	if (shot.startsWith('two:')) {
		const [ia, ib] = shot.slice(4).split(',');
		const a = def.cast.find((c) => c.id === ia)!;
		const bb = def.cast.find((c) => c.id === ib)!;
		return twoShot(a, bb, t, def.front);
	}
	const idx = def.cast.findIndex((c) => c.id === shot);
	if (idx < 0) return def.wides[0](t);
	return closeUp(def.cast[idx], t, def.front, def.cast[idx].side ?? (idx % 2 ? -1 : 1));
};

export const SceneView: React.FC<{def: SceneDef; span: Span; freeze?: number}> = ({def, span, freeze}) => {
	const frame = useCurrentFrame();
	const t = freeze ?? span.from + frame / FPS;
	const b = beatAt(t);
	const shake = Math.max(def.shake ? def.shake(t) : 0, b && b.scene === span.scene && b.shake ? b.shake * (1 - range(t, b.at, b.to)) : 0);
	const cam = withShake(camFor(def, span.scene!, t), t, shake);
	const visible = def.cast.filter((a) => !a.show || a.show(t));
	const items: BB[] = visible
		.filter((a) => a.name !== null && a.kind !== 'kids')
		.map((a) => {
			const p = posOf(a, t);
			const s = a.s ?? 1;
			return {p, h: SIZE[a.kind][2] * s, name: a.name ?? SPEAKER_TAG[a.id]?.[0] ?? a.id, talking: talking(a.id, t)};
		});
	const anyTalk = visible.some((a) => talking(a.id, t));
	return (
		<AbsoluteFill>
			<Stage cam={cam} env={{shadowCenter: def.front, shadowSize: 46, ...def.env}}>
				{def.set ? def.set(t) : null}
				{visible.map((a, i) => (
					<ActorView key={a.id + i} a={a} t={t} front={def.front} />
				))}
			</Stage>
			<Billboards cam={cam} t={t} items={items} />
			{def.over ? def.over(t) : null}
			{freeze === undefined ? (
				<>
					<GameUI t={t} talking={anyTalk} mode="plain" chatFrom={span.from} />
					{BIGS.filter((x) => x.from >= span.from && x.from < span.to).map((x, i) => (
						<BigText key={i} t={t} from={x.from} to={x.to} text={x.text} color={x.color} size={x.size ?? 110} top={x.top ?? 150} />
					))}
					{FLASHES.filter((x) => x.at >= span.from && x.at < span.to).map((x, i) => (
						<Flash key={i} t={t} at={x.at} dur={0.5} color={x.color} />
					))}
					<Fade t={t} inAt={span.from} inDur={0.3} />
				</>
			) : null}
		</AbsoluteFill>
	);
};

// ---------------------------------------------------------------- cards
export const TitleCard: React.FC<{span: Span}> = ({span}) => {
	const t = useCurrentFrame() / FPS;
	const dur = span.to - span.from;
	const title = ease(range(t, 0.5, 1.0));
	const sub = range(t, 1.2, 1.8);
	const out = range(t, dur - 0.5, dur);
	const color = span.color ?? '#ff5b5b';
	return (
		<AbsoluteFill style={{background: '#000'}}>
			<AbsoluteFill style={{background: `radial-gradient(ellipse at 30% 50%, ${color}33, #000 70%)`}} />
			<div style={{position: 'absolute', left: 150, top: 300, opacity: title, transform: `translateX(${(1 - title) * -40}px)`}}>
				<div style={{fontFamily: DOC_FONT, fontSize: 300, color: '#fff', letterSpacing: 30, lineHeight: 1}}>{span.text}</div>
				<div style={{height: 5, width: 700 * title, background: color, marginTop: 10}} />
				<div style={{fontFamily: UI_FONT, fontSize: 46, color: '#fff', marginTop: 24, letterSpacing: 8, opacity: sub, fontWeight: 700}}>{span.sub}</div>
			</div>
			<Grain t={t} />
			<Vignette />
			<Letterbox h={110} />
			<AbsoluteFill style={{background: '#000', opacity: Math.max(1 - t / 0.4, out)}} />
		</AbsoluteFill>
	);
};

export const EndCard: React.FC<{span: Span}> = ({span}) => {
	const t = useCurrentFrame() / FPS;
	const dur = span.to - span.from;
	const letters = (span.text ?? 'THE END').split('');
	const color = span.color ?? '#ff5b5b';
	const out = range(t, dur - 0.5, dur);
	return (
		<AbsoluteFill style={{background: '#000'}}>
			<div style={{position: 'absolute', left: 0, right: 0, top: 260, display: 'flex', justifyContent: 'center', gap: 20}}>
				{letters.map((l, i) => {
					const k = ease(range(t, 0.2 + i * 0.12, 0.6 + i * 0.12));
					return (
						<div key={i} style={{fontFamily: DOC_FONT, fontSize: 260, lineHeight: 1, color: /[0-9+]/.test(l) ? color : '#fff', opacity: k, transform: `translateY(${(1 - k) * -80}px)`, minWidth: l === ' ' ? 50 : 0}}>
							{l}
						</div>
					);
				})}
			</div>
			<div style={{position: 'absolute', left: 0, right: 0, top: 600, textAlign: 'center', fontFamily: DOC_FONT, fontSize: 110, letterSpacing: 18, color: '#fff', opacity: range(t, 1.6, 2.2)}}>{span.sub ?? 'THE END'}</div>
			<Grain t={t} opacity={0.06} />
			<Letterbox />
			<AbsoluteFill style={{background: '#000', opacity: Math.max(1 - t / 0.3, out)}} />
		</AbsoluteFill>
	);
};

/** freeze frame + sepia + the "to be continued" arrow */
export const TbcCard: React.FC<{span: Span; def: SceneDef}> = ({span, def}) => {
	const t = useCurrentFrame() / FPS;
	const dur = span.to - span.from;
	const k = ease(range(t, 0.15, 0.6));
	return (
		<AbsoluteFill style={{background: '#000'}}>
			<AbsoluteFill style={{filter: 'sepia(0.85) contrast(1.15) brightness(0.95)'}}>
				<SceneView def={def} span={span} freeze={span.from - 0.05} />
			</AbsoluteFill>
			<div style={{position: 'absolute', left: 80 - (1 - k) * 900, bottom: 140, display: 'flex', alignItems: 'center'}}>
				<div style={{background: '#f2d33c', color: '#2a2205', fontFamily: UI_FONT, fontWeight: 800, fontSize: 64, padding: '14px 40px', letterSpacing: 2, border: '5px solid #2a2205', borderRight: 'none'}}>TO BE CONTINUED</div>
				<div style={{width: 0, height: 0, borderTop: '58px solid transparent', borderBottom: '58px solid transparent', borderLeft: '80px solid #2a2205', position: 'relative'}}>
					<div style={{position: 'absolute', left: -86, top: -51, width: 0, height: 0, borderTop: '51px solid transparent', borderBottom: '51px solid transparent', borderLeft: '72px solid #f2d33c'}} />
				</div>
			</div>
			<AbsoluteFill style={{background: '#000', opacity: interpolate(t, [dur - 0.4, dur], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})}} />
		</AbsoluteFill>
	);
};
