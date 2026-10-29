import React, {useMemo} from 'react';
import * as THREE from 'three';
import {rbox} from './Avatar';
import {V3} from './cam';
import {checkerTexture, rand, reelTexture, signTexture, SYMBOLS} from './textures';

// ---------------------------------------------------------------- pets
export const Pet: React.FC<{kind: 'cat' | 'dog' | 'dragon'; position: V3; rotationY?: number; t: number; scale?: number}> = ({
	kind,
	position,
	rotationY = 0,
	t,
	scale = 1,
}) => {
	const body = kind === 'cat' ? '#ffb347' : kind === 'dog' ? '#d9a066' : '#8a5cff';
	const ear = kind === 'cat' ? '#ff9f1c' : kind === 'dog' ? '#8b5a2b' : '#ffd23f';
	const bob = Math.sin(t * 4 + position[0]) * 0.25;
	return (
		<group position={[position[0], position[1] + 1.6 + bob, position[2]]} rotation={[0, rotationY, 0]} scale={scale}>
			<mesh geometry={rbox(1.6, 1.4, 1.5, 0.45)} castShadow>
				<meshStandardMaterial color={body} roughness={0.5} />
			</mesh>
			{/* ears */}
			{[-1, 1].map((s) =>
				kind === 'dog' ? (
					<mesh key={s} position={[s * 0.75, 0.15, 0]} geometry={rbox(0.25, 0.9, 0.6, 0.1)} castShadow>
						<meshStandardMaterial color={ear} />
					</mesh>
				) : (
					<mesh key={s} position={[s * 0.45, 0.85, 0]} rotation={[0, Math.PI / 4, 0]} castShadow>
						<coneGeometry args={[0.32, 0.6, 4]} />
						<meshStandardMaterial color={ear} />
					</mesh>
				),
			)}
			{/* eyes */}
			{[-1, 1].map((s) => (
				<group key={s} position={[s * 0.36, 0.12, 0.76]}>
					<mesh>
						<sphereGeometry args={[0.2, 16, 12]} />
						<meshStandardMaterial color="#111" roughness={0.2} />
					</mesh>
					<mesh position={[0.06, 0.07, 0.15]}>
						<sphereGeometry args={[0.06, 8, 6]} />
						<meshStandardMaterial color="#fff" emissive="#fff" emissiveIntensity={0.6} />
					</mesh>
				</group>
			))}
			<mesh position={[0, -0.15, 0.78]}>
				<sphereGeometry args={[0.1, 10, 8]} />
				<meshStandardMaterial color="#ff6b8b" />
			</mesh>
			{kind === 'dragon'
				? [-1, 1].map((s) => (
						<mesh key={s} position={[s * 1.1, 0.3, -0.2]} rotation={[0, 0, s * (0.4 + Math.sin(t * 10) * 0.4)]}>
							<boxGeometry args={[1.2, 0.08, 0.8]} />
							<meshStandardMaterial color="#ffd23f" />
						</mesh>
				  ))
				: null}
			{/* shadow blob */}
			<mesh position={[0, -1.55 - bob, 0]} rotation={[-Math.PI / 2, 0, 0]}>
				<circleGeometry args={[0.8, 20]} />
				<meshBasicMaterial color="#000" transparent opacity={0.18} depthWrite={false} />
			</mesh>
		</group>
	);
};

// ---------------------------------------------------------------- gambling machine
export const Machine: React.FC<{
	position?: V3;
	t: number;
	spin: [number, number, number]; // reel offset in symbols (float)
	lights?: number;
	broken?: boolean;
}> = ({position = [0, 0, 0], t, spin, lights = 1}) => {
	const reel = useMemo(() => reelTexture(), []);
	const reels = useMemo(
		() =>
			[0, 1, 2].map(() => {
				const c = reel.clone();
				c.needsUpdate = true;
				return c;
			}),
		[reel],
	);
	reels.forEach((r, i) => {
		r.offset.y = 1 - ((spin[i] % SYMBOLS.length) + SYMBOLS.length) % SYMBOLS.length / SYMBOLS.length - 1 / SYMBOLS.length;
	});
	const sign = useMemo(() => signTexture('LUCKY SPIN', '#ff2e88', '#ffe14d', 'lucky'), []);
	const floor = useMemo(() => checkerTexture(), []);
	const bulbs = useMemo(() => {
		const out: V3[] = [];
		for (let i = 0; i <= 12; i++) out.push([-6 + i, 13.6, 2.15]);
		for (let i = 0; i <= 10; i++) {
			out.push([-6.3, 3 + i, 2.15]);
			out.push([6.3, 3 + i, 2.15]);
		}
		return out;
	}, []);
	return (
		<group position={position}>
			{/* casino floor */}
			<mesh position={[0, 0.04, 8]} rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
				<planeGeometry args={[34, 30]} />
				<meshStandardMaterial map={floor} roughness={0.35} metalness={0.1} />
			</mesh>
			{/* plinth */}
			<mesh position={[0, 1, 0]} geometry={rbox(15, 2, 6, 0.2)} castShadow receiveShadow>
				<meshStandardMaterial color="#ffc93c" metalness={0.85} roughness={0.25} />
			</mesh>
			{/* body */}
			<mesh position={[0, 8, 0]} geometry={rbox(13, 12, 4, 0.5)} castShadow receiveShadow>
				<meshStandardMaterial color="#b0123e" roughness={0.35} metalness={0.2} />
			</mesh>
			{/* gold trim */}
			<mesh position={[0, 8, 0.1]} geometry={rbox(13.6, 12.6, 3.6, 0.5)}>
				<meshStandardMaterial color="#ffc93c" metalness={0.9} roughness={0.2} />
			</mesh>
			{/* screen bezel */}
			<mesh position={[0, 8.6, 2.05]} geometry={rbox(10.4, 4.6, 0.3, 0.2)}>
				<meshStandardMaterial color="#1b0b24" roughness={0.3} />
			</mesh>
			{reels.map((r, i) => (
				<mesh key={i} position={[(i - 1) * 3.3, 8.6, 2.22]}>
					<planeGeometry args={[3.0, 3.8]} />
					<meshStandardMaterial map={r} emissive="#ffffff" emissiveMap={r} emissiveIntensity={0.45} roughness={0.3} />
				</mesh>
			))}
			{/* win line */}
			<mesh position={[0, 8.6, 2.26]}>
				<planeGeometry args={[10, 0.08]} />
				<meshBasicMaterial color="#ff3355" />
			</mesh>
			{/* sign */}
			<mesh position={[0, 15.6, 0.6]} geometry={rbox(14, 3.6, 1.2, 0.3)} castShadow>
				<meshStandardMaterial color="#ffc93c" metalness={0.85} roughness={0.25} />
			</mesh>
			<mesh position={[0, 15.6, 1.22]}>
				<planeGeometry args={[13.2, 3.0]} />
				<meshStandardMaterial map={sign} emissive="#ffffff" emissiveMap={sign} emissiveIntensity={0.9 * lights} />
			</mesh>
			{/* big 99% badge */}
			<mesh position={[0, 4.4, 2.15]} geometry={rbox(6, 1.6, 0.2, 0.2)}>
				<meshStandardMaterial color="#1b0b24" />
			</mesh>
			<mesh position={[0, 4.4, 2.27]}>
				<planeGeometry args={[5.6, 1.3]} />
				<meshStandardMaterial
					map={signTexture('SPIN 💎 250K', '#2a0a3a', '#7df9ff', 'cost', 1024, 240)}
					emissive="#ffffff"
					emissiveMap={signTexture('SPIN 💎 250K', '#2a0a3a', '#7df9ff', 'cost', 1024, 240)}
					emissiveIntensity={0.7}
				/>
			</mesh>
			{/* lever */}
			<group position={[7.4, 8, 0.5]}>
				<mesh rotation={[0, 0, Math.PI / 2]} position={[0.3, 0, 0]}>
					<cylinderGeometry args={[0.6, 0.6, 0.8, 20]} />
					<meshStandardMaterial color="#ffc93c" metalness={0.9} roughness={0.2} />
				</mesh>
				<mesh position={[0.8, 2, 0]}>
					<cylinderGeometry args={[0.15, 0.15, 4, 10]} />
					<meshStandardMaterial color="#c0c0c0" metalness={0.9} roughness={0.2} />
				</mesh>
				<mesh position={[0.8, 4.2, 0]}>
					<sphereGeometry args={[0.65, 20, 16]} />
					<meshStandardMaterial color="#ff1744" roughness={0.25} />
				</mesh>
			</group>
			{/* bulbs */}
			{bulbs.map((b, i) => {
				const on = (Math.floor(t * 6) + i) % 3 === 0;
				return (
					<mesh key={i} position={b}>
						<sphereGeometry args={[0.22, 10, 8]} />
						<meshStandardMaterial
							color={on ? '#fff6b0' : '#ffb000'}
							emissive={on ? '#ffd84d' : '#552200'}
							emissiveIntensity={(on ? 2.5 : 0.4) * lights}
						/>
					</mesh>
				);
			})}
			<pointLight position={[0, 9, 6]} color="#ff4f9a" intensity={60 * lights} distance={30} decay={1.6} />
			<pointLight position={[0, 15, 5]} color="#ffd84d" intensity={40 * lights} distance={26} decay={1.6} />
		</group>
	);
};

// ---------------------------------------------------------------- wedding
export const Arch: React.FC<{position?: V3}> = ({position = [0, 0, 0]}) => {
	const flowers = useMemo(
		() =>
			new Array(46).fill(0).map((_, i) => {
				const a = (i / 45) * Math.PI;
				const r = 5.6 + (rand(i) - 0.5) * 0.6;
				return {
					p: [Math.cos(a) * r, 6 + Math.sin(a) * r, (rand(i + 2) - 0.5) * 0.8] as V3,
					c: ['#ff7aa8', '#ffffff', '#ff4d6d', '#ffd1dc'][i % 4],
					s: 0.35 + rand(i + 5) * 0.3,
				};
			}),
		[],
	);
	return (
		<group position={position}>
			<mesh position={[0, 6, 0]} castShadow>
				<torusGeometry args={[5.6, 0.35, 12, 48, Math.PI]} />
				<meshStandardMaterial color="#ffffff" roughness={0.5} />
			</mesh>
			{[-5.6, 5.6].map((x) => (
				<mesh key={x} position={[x, 3, 0]} castShadow>
					<cylinderGeometry args={[0.35, 0.45, 6, 16]} />
					<meshStandardMaterial color="#ffffff" roughness={0.5} />
				</mesh>
			))}
			{flowers.map((fl, i) => (
				<mesh key={i} position={fl.p} castShadow>
					<icosahedronGeometry args={[fl.s, 0]} />
					<meshStandardMaterial color={fl.c} roughness={0.6} flatShading />
				</mesh>
			))}
			{/* stage */}
			<mesh position={[0, 0.2, 0]} geometry={rbox(16, 0.4, 8, 0.1)} receiveShadow castShadow>
				<meshStandardMaterial color="#f4ece1" roughness={0.6} />
			</mesh>
		</group>
	);
};

export const Bench: React.FC<{position: V3; rotationY?: number}> = ({position, rotationY = 0}) => (
	<group position={position} rotation={[0, rotationY, 0]}>
		<mesh position={[0, 1.0, 0]} geometry={rbox(8, 0.35, 1.6, 0.08)} castShadow receiveShadow>
			<meshStandardMaterial color="#ffffff" roughness={0.6} />
		</mesh>
		<mesh position={[0, 2.0, -0.8]} geometry={rbox(8, 1.8, 0.3, 0.08)} castShadow>
			<meshStandardMaterial color="#ffffff" roughness={0.6} />
		</mesh>
		{[-3.5, 3.5].map((x) => (
			<mesh key={x} position={[x, 0.5, 0]} geometry={rbox(0.3, 1, 1.4, 0.05)} castShadow>
				<meshStandardMaterial color="#e8e0d4" />
			</mesh>
		))}
		{/* ribbon */}
		<mesh position={[4.05, 2.2, -0.8]}>
			<boxGeometry args={[0.15, 0.6, 0.6]} />
			<meshStandardMaterial color="#ff7aa8" />
		</mesh>
	</group>
);

export const Petals: React.FC<{t: number; center?: V3; count?: number; area?: number; color?: string[]}> = ({
	t,
	center = [0, 0, 0],
	count = 160,
	area = 30,
	color = ['#ff8fb1', '#ffd1dc', '#ffffff'],
}) => {
	const mesh = useMemo(() => {
		const g = new THREE.PlaneGeometry(0.35, 0.25);
		const m = new THREE.MeshStandardMaterial({side: THREE.DoubleSide, roughness: 0.6});
		const im = new THREE.InstancedMesh(g, m, count);
		for (let i = 0; i < count; i++) im.setColorAt(i, new THREE.Color(color[i % color.length]));
		return im;
	}, [count, color]);
	const o = new THREE.Object3D();
	for (let i = 0; i < count; i++) {
		const fall = 1.2 + rand(i) * 1.2;
		const h = 22;
		const y = h - ((t * fall + rand(i + 1) * h) % h);
		o.position.set(
			center[0] + (rand(i + 2) - 0.5) * area + Math.sin(t * 1.3 + i) * 1.2,
			center[1] + y,
			center[2] + (rand(i + 3) - 0.5) * area,
		);
		o.rotation.set(t * 2 + i, t * 1.5 + i * 0.3, t + i);
		o.updateMatrix();
		mesh.setMatrixAt(i, o.matrix);
	}
	mesh.instanceMatrix.needsUpdate = true;
	return <primitive object={mesh} />;
};

export const Rain: React.FC<{t: number; center: V3; count?: number; area?: number; opacity?: number}> = ({
	t,
	center,
	count = 900,
	area = 60,
	opacity = 0.45,
}) => {
	const mesh = useMemo(() => {
		const g = new THREE.BoxGeometry(0.04, 1.6, 0.04);
		const m = new THREE.MeshBasicMaterial({color: '#bcd3ff', transparent: true, opacity});
		return new THREE.InstancedMesh(g, m, count);
	}, [count, opacity]);
	const o = new THREE.Object3D();
	for (let i = 0; i < count; i++) {
		const h = 40;
		const y = h - ((t * 38 + rand(i) * h) % h);
		o.position.set(center[0] + (rand(i + 1) - 0.5) * area, center[1] + y, center[2] + (rand(i + 2) - 0.5) * area);
		o.rotation.set(0, 0, 0.08);
		o.updateMatrix();
		mesh.setMatrixAt(i, o.matrix);
	}
	mesh.instanceMatrix.needsUpdate = true;
	return <primitive object={mesh} />;
};

export const LampPost: React.FC<{position: V3}> = ({position}) => (
	<group position={position}>
		<mesh position={[0, 4, 0]} castShadow>
			<cylinderGeometry args={[0.18, 0.25, 8, 10]} />
			<meshStandardMaterial color="#2b2b30" metalness={0.6} roughness={0.4} />
		</mesh>
		<mesh position={[0, 8.2, 0]}>
			<boxGeometry args={[0.9, 0.9, 0.9]} />
			<meshStandardMaterial color="#fff1c4" emissive="#ffc46b" emissiveIntensity={3} />
		</mesh>
		<pointLight position={[0, 7.6, 0]} color="#ffbe6b" intensity={160} distance={22} decay={1.6} />
	</group>
);

export const Sparkles: React.FC<{points: V3[]; t: number; color?: string; size?: number}> = ({points, t, color = '#fff2a8', size = 0.35}) => (
	<>
		{points.map((p, i) => (
			<mesh key={i} position={p} rotation={[t * 3 + i, t * 2 + i, 0]} scale={size * (0.6 + 0.4 * Math.sin(t * 12 + i))}>
				<octahedronGeometry args={[1, 0]} />
				<meshBasicMaterial color={color} />
			</mesh>
		))}
	</>
);

export const Meteor: React.FC<{from: V3; to: V3; k: number}> = ({from, to, k}) => {
	if (k <= 0 || k >= 1) return null;
	const p: V3 = [from[0] + (to[0] - from[0]) * k, from[1] + (to[1] - from[1]) * k, from[2] + (to[2] - from[2]) * k];
	const dir = new THREE.Vector3(to[0] - from[0], to[1] - from[1], to[2] - from[2]).normalize();
	const q = new THREE.Quaternion().setFromUnitVectors(new THREE.Vector3(0, 1, 0), dir.clone().negate());
	return (
		<group position={p}>
			<mesh>
				<icosahedronGeometry args={[2.2, 1]} />
				<meshStandardMaterial color="#3a1a0a" emissive="#ff5a00" emissiveIntensity={2.2} flatShading />
			</mesh>
			<mesh quaternion={q} position={[-dir.x * 7, -dir.y * 7, -dir.z * 7]}>
				<coneGeometry args={[2.0, 14, 16, 1, true]} />
				<meshBasicMaterial color="#ffb347" transparent opacity={0.55} depthWrite={false} side={THREE.DoubleSide} blending={THREE.AdditiveBlending} />
			</mesh>
			<pointLight color="#ff6a00" intensity={400} distance={60} decay={1.5} />
		</group>
	);
};

// Ground made of tiles that fall away as the collapse front (z0 + v*(t-t0)) sweeps forward.
export const CollapseGround: React.FC<{t: number; t0: number; z0: number; v: number; xHalf?: number; zMin?: number; zMax?: number; tile?: number}> = ({
	t,
	t0,
	z0,
	v,
	xHalf = 72,
	zMin = -160,
	zMax = 150,
	tile = 8,
}) => {
	const tiles = useMemo(() => {
		const out: {x: number; z: number; jitter: number; c: string; i: number}[] = [];
		let i = 0;
		for (let x = -xHalf; x < xHalf; x += tile)
			for (let z = zMin; z < zMax; z += tile) {
				out.push({
					x: x + tile / 2,
					z: z + tile / 2,
					jitter: rand(i) * 1.4 + Math.abs(x) / 70,
					c: ['#4fa13a', '#4a9a36', '#56a840', '#459033'][i % 4],
					i: i++,
				});
			}
		return out;
	}, [xHalf, zMin, zMax, tile]);
	return (
		<>
			{tiles.map((tl) => {
				const fallAt = t0 + (tl.z - z0) / v + tl.jitter;
				const k = Math.max(0, t - fallAt);
				const y = -0.5 * 22 * k * k;
				if (y < -140) return null;
				const rot = k * (rand(tl.i) - 0.5) * 2.5;
				return (
					<mesh key={tl.i} position={[tl.x, -1 + y, tl.z]} rotation={[rot, 0, rot * 0.7]} geometry={rbox(tile - 0.1, 2, tile - 0.1, 0.12)} receiveShadow castShadow={k > 0}>
						<meshStandardMaterial color={tl.c} roughness={0.95} />
					</mesh>
				);
			})}
			{/* glowing magma far below */}
			<mesh position={[0, -90, 0]} rotation={[-Math.PI / 2, 0, 0]}>
				<planeGeometry args={[1400, 1400]} />
				<meshBasicMaterial color="#ff3d00" fog={false} />
			</mesh>
		</>
	);
};

export const Spotlight: React.FC<{position: V3; target: V3; intensity?: number; color?: string}> = ({position, target, intensity = 900, color = '#ffffff'}) => {
	const light = useMemo(() => {
		const l = new THREE.SpotLight(color, intensity, 80, 0.38, 0.6, 1.4);
		l.castShadow = true;
		l.shadow.mapSize.set(1024, 1024);
		return l;
	}, [color, intensity]);
	light.position.set(...position);
	light.target.position.set(...target);
	light.target.updateMatrixWorld();
	return (
		<>
			<primitive object={light} />
			<primitive object={light.target} />
		</>
	);
};
