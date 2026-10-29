import React, {useMemo} from 'react';
import * as THREE from 'three';
import {useThree} from '@react-three/fiber';
import {ThreeCanvas} from '@remotion/three';
import {W, H} from '../timeline';
import {applyCam, Cam, V3} from './cam';
import {grassTexture, rand, spawnTexture} from './textures';
import {rbox} from './Avatar';

export type Env = {
	skyTop: string;
	skyHorizon: string;
	skyBottom?: string;
	sunDir: V3;
	sunColor: string;
	sunIntensity: number;
	hemiSky: string;
	hemiGround: string;
	hemiIntensity: number;
	fog: [string, number, number];
	exposure?: number;
	sunGlow?: number;
	shadowCenter?: V3;
	shadowSize?: number;
	stars?: number;
};

export const DAY: Env = {
	skyTop: '#2f7fe0',
	skyHorizon: '#bfe3ff',
	sunDir: [0.45, 0.8, 0.35],
	sunColor: '#fff4e0',
	sunIntensity: 2.6,
	hemiSky: '#cfe8ff',
	hemiGround: '#5d8f3a',
	hemiIntensity: 1.0,
	fog: ['#cfe8ff', 120, 420],
	sunGlow: 0.6,
};

export const lerpEnv = (a: Env, b: Env, t: number): Env => {
	const c = (x: string, y: string) => '#' + new THREE.Color(x).lerp(new THREE.Color(y), t).getHexString();
	const n = (x: number, y: number) => x + (y - x) * t;
	return {
		...a,
		skyTop: c(a.skyTop, b.skyTop),
		skyHorizon: c(a.skyHorizon, b.skyHorizon),
		sunDir: [n(a.sunDir[0], b.sunDir[0]), n(a.sunDir[1], b.sunDir[1]), n(a.sunDir[2], b.sunDir[2])],
		sunColor: c(a.sunColor, b.sunColor),
		sunIntensity: n(a.sunIntensity, b.sunIntensity),
		hemiSky: c(a.hemiSky, b.hemiSky),
		hemiGround: c(a.hemiGround, b.hemiGround),
		hemiIntensity: n(a.hemiIntensity, b.hemiIntensity),
		fog: [c(a.fog[0], b.fog[0]), n(a.fog[1], b.fog[1]), n(a.fog[2], b.fog[2])],
		exposure: n(a.exposure ?? 1, b.exposure ?? 1),
		sunGlow: n(a.sunGlow ?? 0.6, b.sunGlow ?? 0.6),
		stars: n(a.stars ?? 0, b.stars ?? 0),
	};
};

const CamRig: React.FC<{cam: Cam}> = ({cam}) => {
	const {camera} = useThree();
	applyCam(camera as THREE.PerspectiveCamera, cam);
	return null;
};

const EnvRig: React.FC<{env: Env}> = ({env}) => {
	const {scene, gl} = useThree();
	if (!scene.fog) scene.fog = new THREE.Fog(env.fog[0], env.fog[1], env.fog[2]);
	const fog = scene.fog as THREE.Fog;
	fog.color.set(env.fog[0]);
	fog.near = env.fog[1];
	fog.far = env.fog[2];
	gl.toneMappingExposure = env.exposure ?? 1;
	const center = env.shadowCenter ?? [0, 0, 0];
	const sz = env.shadowSize ?? 40;
	const light = useMemo(() => {
		const l = new THREE.DirectionalLight();
		l.castShadow = true;
		l.shadow.mapSize.set(2048, 2048);
		l.shadow.bias = -0.0004;
		l.shadow.normalBias = 0.03;
		return l;
	}, []);
	light.color.set(env.sunColor);
	light.intensity = env.sunIntensity;
	const d = new THREE.Vector3(...env.sunDir).normalize();
	light.position.set(center[0] + d.x * 120, center[1] + d.y * 120, center[2] + d.z * 120);
	light.target.position.set(...center);
	light.target.updateMatrixWorld();
	const sc = light.shadow.camera;
	sc.left = -sz;
	sc.right = sz;
	sc.top = sz;
	sc.bottom = -sz;
	sc.near = 1;
	sc.far = 400;
	sc.updateProjectionMatrix();
	return (
		<>
			<primitive object={light} />
			<primitive object={light.target} />
			<hemisphereLight args={[env.hemiSky, env.hemiGround, env.hemiIntensity]} />
			<Sky env={env} />
		</>
	);
};

const skyVert = `
varying vec3 vDir;
void main(){
  vDir = normalize((modelMatrix * vec4(position,1.0)).xyz - cameraPosition);
  vec4 p = projectionMatrix * modelViewMatrix * vec4(position,1.0);
  gl_Position = p.xyww;
}`;
const skyFrag = `
uniform vec3 top; uniform vec3 horizon; uniform vec3 bottom; uniform vec3 sunDir; uniform vec3 sunColor; uniform float glow; uniform float stars;
varying vec3 vDir;
float hash(vec3 p){ return fract(sin(dot(p, vec3(12.9898,78.233,45.164)))*43758.5453); }
void main(){
  vec3 d = normalize(vDir);
  float h = d.y;
  vec3 col = h > 0.0 ? mix(horizon, top, pow(clamp(h,0.0,1.0), 0.55)) : mix(horizon, bottom, clamp(-h*3.0,0.0,1.0));
  float s = max(dot(d, normalize(sunDir)), 0.0);
  col += sunColor * (pow(s, 900.0) * 3.0 + pow(s, 12.0) * 0.35 * glow + pow(s, 3.0) * 0.12 * glow);
  if (stars > 0.0 && h > 0.0) {
    vec3 q = floor(d * 420.0);
    float st = step(0.9975, hash(q));
    col += vec3(st) * stars * h;
  }
  gl_FragColor = vec4(col, 1.0);
  #include <tonemapping_fragment>
  #include <colorspace_fragment>
}`;

const Sky: React.FC<{env: Env}> = ({env}) => {
	const material = useMemo(
		() =>
			new THREE.ShaderMaterial({
				vertexShader: skyVert,
				fragmentShader: skyFrag,
				side: THREE.BackSide,
				depthWrite: false,
				fog: false,
				uniforms: {
					top: {value: new THREE.Color()},
					horizon: {value: new THREE.Color()},
					bottom: {value: new THREE.Color()},
					sunDir: {value: new THREE.Vector3()},
					sunColor: {value: new THREE.Color()},
					glow: {value: 0.6},
					stars: {value: 0},
				},
			}),
		[],
	);
	material.uniforms.top.value.set(env.skyTop);
	material.uniforms.horizon.value.set(env.skyHorizon);
	material.uniforms.bottom.value.set(env.skyBottom ?? env.fog[0]);
	material.uniforms.sunDir.value.set(...env.sunDir);
	material.uniforms.sunColor.value.set(env.sunColor);
	material.uniforms.glow.value = env.sunGlow ?? 0.6;
	material.uniforms.stars.value = env.stars ?? 0;
	return (
		<mesh material={material} renderOrder={-1} frustumCulled={false}>
			<sphereGeometry args={[900, 32, 16]} />
		</mesh>
	);
};

export const Stage: React.FC<{cam: Cam; env: Env; children: React.ReactNode}> = ({cam, env, children}) => (
	<ThreeCanvas
		width={W}
		height={H}
		shadows={{type: THREE.PCFSoftShadowMap}}
		gl={{antialias: true, preserveDrawingBuffer: true}}
		camera={{near: 0.1, far: 2000, fov: cam.fov}}
		style={{position: 'absolute', inset: 0}}
	>
		<CamRig cam={cam} />
		<EnvRig env={env} />
		{children}
	</ThreeCanvas>
);

// ---------------------------------------------------------------- props
export const Ground: React.FC<{color?: string; size?: number}> = ({color = '#ffffff', size = 900}) => {
	const tex = useMemo(() => grassTexture(), []);
	return (
		<mesh rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
			<planeGeometry args={[size, size]} />
			<meshStandardMaterial map={tex} color={color} roughness={0.95} />
		</mesh>
	);
};

export const Path: React.FC<{from: V3; to: V3; width?: number; color?: string}> = ({from, to, width = 8, color = '#d9c08a'}) => {
	const dx = to[0] - from[0];
	const dz = to[2] - from[2];
	const len = Math.hypot(dx, dz);
	return (
		<mesh
			position={[(from[0] + to[0]) / 2, 0.03, (from[2] + to[2]) / 2]}
			rotation={[-Math.PI / 2, 0, Math.atan2(dx, dz)]}
			receiveShadow
		>
			<planeGeometry args={[width, len]} />
			<meshStandardMaterial color={color} roughness={0.95} />
		</mesh>
	);
};

export const Tree: React.FC<{position: V3; s?: number; seed?: number; color?: string}> = ({position, s = 1, seed = 0, color}) => {
	const leaf = color ?? ['#3e9b3a', '#4caf50', '#2e7d32', '#5cb85c'][seed % 4];
	return (
		<group position={position} scale={s} rotation={[0, seed, 0]}>
			<mesh position={[0, 3, 0]} geometry={rbox(1.4, 6, 1.4, 0.15)} castShadow receiveShadow>
				<meshStandardMaterial color="#7a5230" roughness={0.9} />
			</mesh>
			<mesh position={[0, 7.4, 0]} castShadow receiveShadow>
				<icosahedronGeometry args={[3.6, 0]} />
				<meshStandardMaterial color={leaf} roughness={0.85} flatShading />
			</mesh>
			<mesh position={[1.6, 6.2, 0.8]} castShadow>
				<icosahedronGeometry args={[2.2, 0]} />
				<meshStandardMaterial color={leaf} roughness={0.85} flatShading />
			</mesh>
			<mesh position={[-1.4, 6.6, -0.9]} castShadow>
				<icosahedronGeometry args={[2.4, 0]} />
				<meshStandardMaterial color={leaf} roughness={0.85} flatShading />
			</mesh>
		</group>
	);
};

export const Forest: React.FC<{count?: number; radius?: [number, number]; seed?: number; avoid?: (x: number, z: number) => boolean}> = ({
	count = 40,
	radius = [45, 160],
	seed = 1,
	avoid,
}) => {
	const trees = useMemo(() => {
		const out: {p: V3; s: number; i: number}[] = [];
		for (let i = 0; out.length < count && i < count * 6; i++) {
			const a = rand(seed * 100 + i) * Math.PI * 2;
			const r = radius[0] + rand(seed * 100 + i + 0.3) * (radius[1] - radius[0]);
			const x = Math.cos(a) * r;
			const z = Math.sin(a) * r;
			if (avoid && avoid(x, z)) continue;
			out.push({p: [x, 0, z], s: 0.8 + rand(i + 7) * 0.7, i});
		}
		return out;
	}, [count, radius, seed, avoid]);
	return (
		<>
			{trees.map((t) => (
				<Tree key={t.i} position={t.p} s={t.s} seed={t.i} />
			))}
		</>
	);
};

export const Clouds: React.FC<{t: number; color?: string; opacity?: number}> = ({t, color = '#ffffff', opacity = 0.92}) => {
	const clouds = useMemo(
		() =>
			new Array(14).fill(0).map((_, i) => ({
				x: (rand(i) - 0.5) * 600,
				y: 70 + rand(i + 1) * 40,
				z: -100 - rand(i + 2) * 300,
				w: 30 + rand(i + 3) * 40,
				d: 14 + rand(i + 4) * 16,
			})),
		[],
	);
	return (
		<>
			{clouds.map((c, i) => (
				<group key={i} position={[((c.x + t * 1.5 + 300) % 600) - 300, c.y, c.z]}>
					<mesh geometry={rbox(c.w, 5, c.d, 2)}>
						<meshStandardMaterial color={color} transparent opacity={opacity} roughness={1} />
					</mesh>
					<mesh position={[c.w * 0.15, 3, 0]} geometry={rbox(c.w * 0.5, 5, c.d * 0.7, 2)}>
						<meshStandardMaterial color={color} transparent opacity={opacity} roughness={1} />
					</mesh>
				</group>
			))}
		</>
	);
};

export const SpawnPad: React.FC<{position?: V3}> = ({position = [0, 0, 0]}) => {
	const tex = useMemo(() => spawnTexture(), []);
	return (
		<group position={position}>
			<mesh position={[0, 0.25, 0]} geometry={rbox(12, 0.5, 12, 0.1)} receiveShadow castShadow>
				<meshStandardMaterial color="#a3a2a5" roughness={0.7} />
			</mesh>
			<mesh position={[0, 0.51, 0]} rotation={[-Math.PI / 2, 0, 0]}>
				<planeGeometry args={[11, 11]} />
				<meshStandardMaterial map={tex} roughness={0.7} />
			</mesh>
		</group>
	);
};

export const Diamond: React.FC<{position: V3; t: number; scale?: number}> = ({position, t, scale = 1}) => (
	<group position={[position[0], position[1] + 1.2 + Math.sin(t * 3 + position[0]) * 0.25, position[2]]} rotation={[0, t * 2.2, 0]} scale={scale}>
		<mesh castShadow>
			<octahedronGeometry args={[0.9, 0]} />
			<meshStandardMaterial color="#5ee7ff" emissive="#1fb6ff" emissiveIntensity={0.6} metalness={0.3} roughness={0.15} flatShading />
		</mesh>
	</group>
);

export const CoinPile: React.FC<{position: V3}> = ({position}) => (
	<group position={position}>
		{new Array(9).fill(0).map((_, i) => (
			<mesh key={i} position={[(rand(i) - 0.5) * 2, 0.15 + i * 0.12, (rand(i + 3) - 0.5) * 2]} rotation={[0.1 * i, rand(i) * 3, 0]} castShadow>
				<cylinderGeometry args={[0.6, 0.6, 0.15, 20]} />
				<meshStandardMaterial color="#ffc93c" metalness={0.75} roughness={0.25} />
			</mesh>
		))}
	</group>
);

export const Fence: React.FC<{from: V3; to: V3; color?: string}> = ({from, to, color = '#ffffff'}) => {
	const dx = to[0] - from[0];
	const dz = to[2] - from[2];
	const len = Math.hypot(dx, dz);
	const n = Math.max(2, Math.round(len / 4));
	const ang = Math.atan2(dx, dz);
	return (
		<group position={from} rotation={[0, ang, 0]}>
			{new Array(n + 1).fill(0).map((_, i) => (
				<mesh key={i} position={[0, 1.2, (i / n) * len]} geometry={rbox(0.5, 2.4, 0.5, 0.08)} castShadow>
					<meshStandardMaterial color={color} />
				</mesh>
			))}
			<mesh position={[0, 1.7, len / 2]} geometry={rbox(0.3, 0.35, len, 0.05)} castShadow>
				<meshStandardMaterial color={color} />
			</mesh>
			<mesh position={[0, 0.9, len / 2]} geometry={rbox(0.3, 0.35, len, 0.05)} castShadow>
				<meshStandardMaterial color={color} />
			</mesh>
		</group>
	);
};

export const Flowers: React.FC<{center: V3; radius: number; count?: number; seed?: number}> = ({center, radius, count = 40, seed = 3}) => {
	const items = useMemo(
		() =>
			new Array(count).fill(0).map((_, i) => {
				const a = rand(seed + i) * Math.PI * 2;
				const r = Math.sqrt(rand(seed + i + 0.5)) * radius;
				return {
					p: [center[0] + Math.cos(a) * r, 0, center[2] + Math.sin(a) * r] as V3,
					c: ['#ff5c8a', '#ffd23f', '#ffffff', '#b26bff', '#ff8c42'][i % 5],
				};
			}),
		[center, radius, count, seed],
	);
	return (
		<>
			{items.map((it, i) => (
				<group key={i} position={it.p}>
					<mesh position={[0, 0.4, 0]}>
						<boxGeometry args={[0.12, 0.8, 0.12]} />
						<meshStandardMaterial color="#2e7d32" />
					</mesh>
					<mesh position={[0, 0.85, 0]} castShadow>
						<boxGeometry args={[0.5, 0.3, 0.5]} />
						<meshStandardMaterial color={it.c} roughness={0.6} />
					</mesh>
				</group>
			))}
		</>
	);
};
