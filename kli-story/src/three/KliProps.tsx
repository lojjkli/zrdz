import React, {useMemo} from 'react';
import * as THREE from 'three';
import {V3} from './cam';
import {canvasTex, rand} from './textures';
import {rbox} from './Avatar';

const std = (color: string, extra: Partial<THREE.MeshStandardMaterialParameters> = {}) => <meshStandardMaterial color={color} roughness={0.6} {...extra} />;

// ---------------------------------------------------------------- textures
export const baseplateTexture = (key: string, base = '#6b6e72', line = '#5a5d61', repeat = 40) =>
	canvasTex(
		'bp-' + key,
		128,
		128,
		(ctx) => {
			ctx.fillStyle = base;
			ctx.fillRect(0, 0, 128, 128);
			ctx.strokeStyle = line;
			ctx.lineWidth = 3;
			ctx.strokeRect(1.5, 1.5, 125, 125);
		},
		{repeat: [repeat, repeat]},
	);

const brickTexture = () =>
	canvasTex(
		'brick',
		256,
		256,
		(ctx) => {
			ctx.fillStyle = '#4a2a24';
			ctx.fillRect(0, 0, 256, 256);
			for (let r = 0; r < 8; r++)
				for (let c = 0; c < 5; c++) {
					const x = c * 56 + (r % 2) * 28 - 28;
					ctx.fillStyle = ['#7a3b2e', '#6d342a', '#843f30', '#5f2e25'][Math.floor(rand(r * 7 + c) * 4)];
					ctx.fillRect(x + 2, r * 32 + 2, 52, 28);
				}
		},
		{repeat: [6, 3]},
	);

// ---------------------------------------------------------------- alley (poor kli lives here)
export const Alley: React.FC<{wet?: number}> = ({wet = 1}) => {
	const brick = useMemo(() => brickTexture(), []);
	const ground = useMemo(() => baseplateTexture('asphalt', '#2c2e33', '#26282c', 30), []);
	return (
		<group>
			<mesh rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
				<planeGeometry args={[200, 200]} />
				<meshStandardMaterial map={ground} roughness={1 - wet * 0.65} metalness={wet * 0.25} />
			</mesh>
			{/* walls */}
			<mesh position={[-9, 9, -2]} castShadow receiveShadow>
				<boxGeometry args={[2, 18, 40]} />
				<meshStandardMaterial map={brick} roughness={0.9} />
			</mesh>
			<mesh position={[0, 9, -14]} receiveShadow>
				<boxGeometry args={[20, 18, 2]} />
				<meshStandardMaterial map={brick} roughness={0.9} />
			</mesh>
			<mesh position={[9, 9, -8]} castShadow receiveShadow>
				<boxGeometry args={[2, 18, 14]} />
				<meshStandardMaterial map={brick} roughness={0.9} />
			</mesh>
			{/* puddles */}
			{[
				[2, 4, 3],
				[-4, 8, 2.2],
				[5, 10, 1.6],
			].map(([x, z, r], i) => (
				<mesh key={i} position={[x, 0.02, z]} rotation={[-Math.PI / 2, 0, 0]}>
					<circleGeometry args={[r, 24]} />
					<meshStandardMaterial color="#1a2236" roughness={0.05} metalness={0.6} />
				</mesh>
			))}
			<TrashCan position={[-6.5, 0, -9]} />
			<TrashCan position={[-6.4, 0, -6.2]} tilt />
		</group>
	);
};

export const TrashCan: React.FC<{position: V3; tilt?: boolean}> = ({position, tilt}) => (
	<group position={position} rotation={[0, 0, tilt ? 0.12 : 0]}>
		<mesh position={[0, 1.4, 0]} castShadow receiveShadow>
			<cylinderGeometry args={[1, 0.9, 2.8, 16]} />
			{std('#59616b', {metalness: 0.6, roughness: 0.45})}
		</mesh>
		<mesh position={[0.1, 2.9, 0]} rotation={[0, 0, tilt ? -0.5 : 0.05]} castShadow>
			<cylinderGeometry args={[1.08, 1.08, 0.18, 16]} />
			{std('#4a5059', {metalness: 0.6, roughness: 0.4})}
		</mesh>
	</group>
);

/** Open cardboard box kli lives in (he sits inside, facing +z). */
export const CardboardBox: React.FC<{position: V3}> = ({position}) => {
	const c = '#b5834a';
	const d = '#9b6c39';
	const W = 4.2;
	const D = 3.6;
	const H = 2.2;
	return (
		<group position={position}>
			<mesh position={[0, 0.06, 0]} receiveShadow>
				<boxGeometry args={[W, 0.12, D]} />
				{std(d)}
			</mesh>
			{/* back + sides (front open) */}
			<mesh position={[0, H / 2, -D / 2]} castShadow receiveShadow>
				<boxGeometry args={[W, H, 0.1]} />
				{std(c)}
			</mesh>
			{[-1, 1].map((s) => (
				<mesh key={s} position={[(s * W) / 2, H / 2, 0]} castShadow receiveShadow>
					<boxGeometry args={[0.1, H, D]} />
					{std(c)}
				</mesh>
			))}
			{/* flaps */}
			{[-1, 1].map((s) => (
				<mesh key={'f' + s} position={[s * (W / 2 + 0.7), H + 0.25, 0]} rotation={[0, 0, s * -0.55]} castShadow>
					<boxGeometry args={[1.6, 0.08, D]} />
					{std(d)}
				</mesh>
			))}
			<mesh position={[0, H + 0.6, -D / 2 - 0.4]} rotation={[0.7, 0, 0]} castShadow>
				<boxGeometry args={[W, 0.08, 1.4]} />
				{std(d)}
			</mesh>
		</group>
	);
};

export const Bread: React.FC<{position: V3; rotationY?: number; scale?: number}> = ({position, rotationY = 0, scale = 1}) => (
	<group position={position} rotation={[0, rotationY, 0.2]} scale={scale}>
		<mesh geometry={rbox(1.1, 0.55, 0.6, 0.22)} castShadow>
			{std('#d39445')}
		</mesh>
		<mesh position={[0, 0.2, 0]} geometry={rbox(1.0, 0.25, 0.55, 0.12)}>
			{std('#a8662a')}
		</mesh>
	</group>
);

export const Pigeon: React.FC<{position: V3; rotationY?: number; t: number; flap?: number; scale?: number}> = ({position, rotationY = 0, t, flap = 1, scale = 1}) => {
	const w = Math.sin(t * 28) * 0.9 * flap;
	return (
		<group position={position} rotation={[0, rotationY, 0]} scale={scale}>
			<mesh geometry={rbox(0.7, 0.6, 1.1, 0.25)} castShadow>
				{std('#8e96a3')}
			</mesh>
			<mesh position={[0, 0.45, 0.55]} geometry={rbox(0.45, 0.45, 0.45, 0.18)} castShadow>
				{std('#6f7a8a')}
			</mesh>
			<mesh position={[0, 0.2, 0.42]} geometry={rbox(0.5, 0.25, 0.2, 0.08)}>
				{std('#5c8f7d', {metalness: 0.5, roughness: 0.3})}
			</mesh>
			<mesh position={[0, 0.4, 0.85]} geometry={rbox(0.14, 0.12, 0.25, 0.04)}>
				{std('#f2a03d')}
			</mesh>
			{[-1, 1].map((s) => (
				<mesh key={s} position={[s * 0.2, 0.55, 0.75]} geometry={rbox(0.08, 0.1, 0.06, 0.02)}>
					{std('#ff5a1f', {emissive: '#ff3a00', emissiveIntensity: 0.4})}
				</mesh>
			))}
			{[-1, 1].map((s) => (
				<group key={'w' + s} position={[s * 0.35, 0.15, 0]} rotation={[0, 0, s * w]}>
					<mesh position={[s * 0.5, 0, 0]} geometry={rbox(1.0, 0.08, 0.8, 0.03)} castShadow>
						{std('#7b8594')}
					</mesh>
				</group>
			))}
			<mesh position={[0, -0.05, -0.65]} rotation={[0.3, 0, 0]} geometry={rbox(0.5, 0.06, 0.5, 0.02)}>
				{std('#4d5563')}
			</mesh>
		</group>
	);
};

// ---------------------------------------------------------------- the magic 3D app orb (orange ring, blue core)
export const Orb: React.FC<{position: V3; t: number; scale?: number}> = ({position, t, scale = 1}) => (
	<group position={position} scale={scale} rotation={[0, t * 1.2, 0]}>
		<mesh>
			<sphereGeometry args={[1, 32, 20]} />
			<meshStandardMaterial color="#2f6fd6" emissive="#2a6cff" emissiveIntensity={0.9} roughness={0.25} />
		</mesh>
		<mesh rotation={[Math.PI / 2, 0, 0]}>
			<torusGeometry args={[1.7, 0.42, 16, 48]} />
			<meshStandardMaterial color="#ff8a1f" emissive="#ff7a00" emissiveIntensity={0.8} roughness={0.3} />
		</mesh>
		<mesh rotation={[0.35, 0.6, 0.2]}>
			<torusGeometry args={[2.3, 0.08, 8, 64]} />
			<meshBasicMaterial color="#ffd8a8" />
		</mesh>
		<pointLight color="#ffb060" intensity={60} distance={14} decay={1.5} />
	</group>
);

// ---------------------------------------------------------------- donut (the famous tutorial one)
export const Donut: React.FC<{position: V3; rotation?: V3; scale?: number}> = ({position, rotation = [0, 0, 0], scale = 1}) => {
	const sprinkles = useMemo(() => {
		const g = new THREE.BoxGeometry(0.06, 0.06, 0.22);
		const m = new THREE.MeshStandardMaterial({roughness: 0.5});
		const n = 120;
		const mesh = new THREE.InstancedMesh(g, m, n);
		const o = new THREE.Object3D();
		const cols = ['#ffffff', '#ffd23f', '#3fc1ff', '#7cff6b', '#ff5a8a', '#b07bff'].map((c) => new THREE.Color(c));
		for (let i = 0; i < n; i++) {
			const u = rand(i) * Math.PI * 2;
			const v = rand(i + 50) * Math.PI * 0.85 + 0.15; // top half of the tube
			const R = 1;
			const r = 0.46;
			o.position.set((R + r * Math.cos(v)) * Math.cos(u), (R + r * Math.cos(v)) * Math.sin(u), r * Math.sin(v) + 0.04);
			o.rotation.set(rand(i + 3) * 3, rand(i + 4) * 3, rand(i + 5) * 3);
			o.updateMatrix();
			mesh.setMatrixAt(i, o.matrix);
			mesh.setColorAt(i, cols[i % cols.length]);
		}
		return mesh;
	}, []);
	return (
		<group position={position} rotation={rotation} scale={scale}>
			<group rotation={[-Math.PI / 2, 0, 0]}>
				<mesh castShadow receiveShadow>
					<torusGeometry args={[1, 0.45, 24, 48]} />
					<meshStandardMaterial color="#d79a55" roughness={0.75} />
				</mesh>
				{/* icing: a slightly thinner torus nudged up so it shows on top */}
				<mesh position={[0, 0, 0.09]} castShadow>
					<torusGeometry args={[1, 0.425, 24, 48]} />
					<meshStandardMaterial color="#ff7fb6" roughness={0.3} />
				</mesh>
				<primitive object={sprinkles} />
			</group>
		</group>
	);
};

// Simple icing donut without clipping (used for the giant rolling one — cheaper + no clipping planes needed)
export const RollingDonut: React.FC<{position: V3; roll: number; yaw?: number; scale?: number}> = ({position, roll, yaw = 0, scale = 1}) => (
	<group position={position} rotation={[0, yaw, 0]} scale={scale}>
		<group rotation={[roll, 0, 0]}>
			<group rotation={[0, Math.PI / 2, 0]}>
				<mesh castShadow>
					<torusGeometry args={[1, 0.45, 20, 40]} />
					<meshStandardMaterial color="#d79a55" roughness={0.75} />
				</mesh>
				<mesh position={[0, 0, 0.06]} castShadow>
					<torusGeometry args={[1, 0.43, 20, 40]} />
					<meshStandardMaterial color="#ff7fb6" roughness={0.3} />
				</mesh>
			</group>
		</group>
	</group>
);

// ---------------------------------------------------------------- rich stuff
export const GoldMansion: React.FC<{position: V3; rotationY?: number}> = ({position, rotationY = 0}) => {
	const gold = {color: '#e8b423', metalness: 0.85, roughness: 0.25};
	return (
		<group position={position} rotation={[0, rotationY, 0]}>
			<mesh position={[0, 7, 0]} castShadow receiveShadow>
				<boxGeometry args={[34, 14, 16]} />
				<meshStandardMaterial {...gold} />
			</mesh>
			<mesh position={[0, 16.5, 0]} castShadow>
				<boxGeometry args={[24, 5, 12]} />
				<meshStandardMaterial {...gold} />
			</mesh>
			<mesh position={[0, 21, 0]} rotation={[0, Math.PI / 4, 0]} castShadow>
				<coneGeometry args={[9, 6, 4]} />
				<meshStandardMaterial color="#fff2b0" metalness={0.9} roughness={0.2} />
			</mesh>
			{/* columns */}
			{[-12, -6, 0, 6, 12].map((x) => (
				<mesh key={x} position={[x, 7, 8.8]} castShadow>
					<cylinderGeometry args={[0.8, 0.9, 14, 16]} />
					<meshStandardMaterial color="#fff6d6" metalness={0.3} roughness={0.35} />
				</mesh>
			))}
			{/* windows */}
			{[-10, 10].map((x) =>
				[4, 10].map((y) => (
					<mesh key={x + '-' + y} position={[x, y, 8.05]}>
						<planeGeometry args={[4, 3.2]} />
						<meshStandardMaterial color="#9fe3ff" emissive="#9fe3ff" emissiveIntensity={0.5} metalness={0.4} roughness={0.1} />
					</mesh>
				)),
			)}
			<mesh position={[0, 3.5, 8.05]}>
				<planeGeometry args={[5, 7]} />
				<meshStandardMaterial color="#5a3a12" />
			</mesh>
			{/* big $ sign */}
			<mesh position={[0, 16.5, 6.05]}>
				<planeGeometry args={[4.5, 4.5]} />
				<meshBasicMaterial map={dollarTex()} transparent />
			</mesh>
		</group>
	);
};

const dollarTex = () =>
	canvasTex('dollar', 256, 256, (ctx) => {
		ctx.clearRect(0, 0, 256, 256);
		ctx.font = '700 230px "Fredoka", sans-serif';
		ctx.textAlign = 'center';
		ctx.textBaseline = 'middle';
		ctx.lineWidth = 16;
		ctx.strokeStyle = '#6b4a00';
		ctx.strokeText('$', 128, 138);
		ctx.fillStyle = '#fff6c2';
		ctx.fillText('$', 128, 138);
	});

export const Car: React.FC<{position: V3; rotationY?: number; color?: string; squash?: number}> = ({position, rotationY = 0, color = '#e8b423', squash = 0}) => (
	<group position={position} rotation={[0, rotationY, 0]} scale={[1 + squash * 0.4, 1 - squash * 0.85, 1 + squash * 0.2]}>
		<mesh position={[0, 1.1, 0]} geometry={rbox(4.4, 1.2, 8.4, 0.3)} castShadow receiveShadow>
			<meshStandardMaterial color={color} metalness={0.8} roughness={0.25} />
		</mesh>
		<mesh position={[0, 2.2, -0.6]} geometry={rbox(3.8, 1.2, 4.2, 0.3)} castShadow>
			<meshStandardMaterial color="#1c2733" metalness={0.5} roughness={0.15} />
		</mesh>
		{[
			[-2.1, 2.8],
			[2.1, 2.8],
			[-2.1, -2.8],
			[2.1, -2.8],
		].map(([x, z], i) => (
			<mesh key={i} position={[x, 0.75, z]} rotation={[0, 0, Math.PI / 2]} castShadow>
				<cylinderGeometry args={[0.75, 0.75, 0.6, 18]} />
				<meshStandardMaterial color="#141414" roughness={0.8} />
			</mesh>
		))}
		{[-1.4, 1.4].map((x) => (
			<mesh key={x} position={[x, 1.2, 4.22]}>
				<planeGeometry args={[0.9, 0.45]} />
				<meshBasicMaterial color="#fffbe0" />
			</mesh>
		))}
	</group>
);

/** Falling Robux bills. */
export const CashRain: React.FC<{t: number; center: V3; count?: number; area?: number; k?: number}> = ({t, center, count = 160, area = 40, k = 1}) => {
	const mesh = useMemo(() => {
		const g = new THREE.PlaneGeometry(0.9, 0.45);
		const m = new THREE.MeshStandardMaterial({color: '#4fd16b', side: THREE.DoubleSide, roughness: 0.6, emissive: '#1a5a24', emissiveIntensity: 0.3});
		return new THREE.InstancedMesh(g, m, count);
	}, [count]);
	const o = new THREE.Object3D();
	const n = Math.floor(count * k);
	for (let i = 0; i < count; i++) {
		const h = 26;
		const y = i < n ? h - ((t * 5 + rand(i) * h) % h) : -50;
		o.position.set(center[0] + (rand(i + 1) - 0.5) * area + Math.sin(t * 2 + i) * 0.6, center[1] + y, center[2] + (rand(i + 2) - 0.5) * area);
		o.rotation.set(t * 3 + i, t * 2.2 + i * 0.7, Math.sin(t * 4 + i));
		o.updateMatrix();
		mesh.setMatrixAt(i, o.matrix);
	}
	mesh.instanceMatrix.needsUpdate = true;
	return <primitive object={mesh} />;
};

// ---------------------------------------------------------------- studio / obby bits
export const Part: React.FC<{position: V3; size: V3; color: string; rotation?: V3}> = ({position, size, color, rotation = [0, 0, 0]}) => (
	<mesh position={position} rotation={rotation} castShadow receiveShadow>
		<boxGeometry args={size} />
		<meshStandardMaterial color={color} roughness={0.7} />
	</mesh>
);

export const Lava: React.FC<{t: number; y?: number}> = ({t, y = 0}) => {
	const tex = useMemo(
		() =>
			canvasTex(
				'lava',
				256,
				256,
				(ctx) => {
					ctx.fillStyle = '#ff4a00';
					ctx.fillRect(0, 0, 256, 256);
					for (let i = 0; i < 70; i++) {
						ctx.fillStyle = rand(i) > 0.5 ? 'rgba(255,220,60,0.55)' : 'rgba(150,20,0,0.5)';
						ctx.beginPath();
						ctx.arc(rand(i + 1) * 256, rand(i + 2) * 256, 6 + rand(i + 3) * 26, 0, Math.PI * 2);
						ctx.fill();
					}
				},
				{repeat: [10, 10]},
			),
		[],
	);
	tex.offset.set(t * 0.02, t * 0.03);
	return (
		<mesh position={[0, y, 0]} rotation={[-Math.PI / 2, 0, 0]}>
			<planeGeometry args={[300, 300]} />
			<meshBasicMaterial map={tex} />
		</mesh>
	);
};

// ---------------------------------------------------------------- blender-ish viewport
const GRID_LINES = (() => {
	const pts: number[] = [];
	for (let i = -40; i <= 40; i++) {
		pts.push(i, 0, -40, i, 0, 40, -40, 0, i, 40, 0, i);
	}
	return new Float32Array(pts);
})();

export const ViewportGrid: React.FC = () => {
	const geo = useMemo(() => {
		const g = new THREE.BufferGeometry();
		g.setAttribute('position', new THREE.BufferAttribute(GRID_LINES, 3));
		return g;
	}, []);
	return (
		<group>
			<lineSegments geometry={geo}>
				<lineBasicMaterial color="#545454" fog={false} />
			</lineSegments>
			<mesh position={[0, 0.005, 0]}>
				<boxGeometry args={[80, 0.01, 0.06]} />
				<meshBasicMaterial color="#c4334a" fog={false} />
			</mesh>
			<mesh position={[0, 0.005, 0]}>
				<boxGeometry args={[0.06, 0.01, 80]} />
				<meshBasicMaterial color="#6f9a24" fog={false} />
			</mesh>
		</group>
	);
};

/** The default cube, selected (orange outline). */
export const DefaultCube: React.FC<{position?: V3; scale?: number; selected?: boolean}> = ({position = [0, 1, 0], scale = 1, selected = true}) =>
	scale <= 0 ? null : (
		<group position={position} scale={scale}>
			<mesh castShadow receiveShadow>
				<boxGeometry args={[2, 2, 2]} />
				<meshStandardMaterial color="#9c9c9c" roughness={0.5} />
			</mesh>
			{selected ? (
				<lineSegments>
					<edgesGeometry args={[new THREE.BoxGeometry(2.02, 2.02, 2.02)]} />
					<lineBasicMaterial color="#ffa21a" />
				</lineSegments>
			) : null}
		</group>
	);
