import * as THREE from 'three';
import {W, H} from '../timeline';

export type V3 = [number, number, number];
export type Cam = {pos: V3; target: V3; fov: number; roll?: number};

export const lerp = (a: number, b: number, t: number) => a + (b - a) * t;
export const lerp3 = (a: V3, b: V3, t: number): V3 => [lerp(a[0], b[0], t), lerp(a[1], b[1], t), lerp(a[2], b[2], t)];
export const clamp01 = (x: number) => Math.min(1, Math.max(0, x));
export const ease = (x: number) => {
	const t = clamp01(x);
	return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
};
export const easeOut = (x: number) => 1 - Math.pow(1 - clamp01(x), 3);
export const range = (t: number, a: number, b: number) => clamp01((t - a) / (b - a));

// Deterministic camera shake from layered sines.
export const shake = (t: number, amt: number): V3 => [
	(Math.sin(t * 37.1) + Math.sin(t * 23.7 + 1.3) * 0.6) * amt,
	(Math.sin(t * 41.3 + 0.7) + Math.sin(t * 19.1 + 2.1) * 0.6) * amt,
	(Math.sin(t * 29.9 + 2.9)) * amt * 0.5,
];

const tmpCam = new THREE.PerspectiveCamera(50, W / H, 0.1, 2000);

export const applyCam = (c: THREE.PerspectiveCamera, cam: Cam) => {
	c.position.set(...cam.pos);
	c.fov = cam.fov;
	c.aspect = W / H;
	c.up.set(0, 1, 0);
	c.lookAt(...cam.target);
	if (cam.roll) c.rotateZ(cam.roll);
	c.updateProjectionMatrix();
	c.updateMatrixWorld();
};

/** Project world point to screen pixels. Returns null if behind camera. */
export const project = (cam: Cam, p: V3): {x: number; y: number; dist: number} | null => {
	applyCam(tmpCam, cam);
	const v = new THREE.Vector3(...p);
	const dist = v.distanceTo(tmpCam.position);
	v.project(tmpCam);
	if (v.z > 1) return null;
	return {x: (v.x * 0.5 + 0.5) * W, y: (-v.y * 0.5 + 0.5) * H, dist};
};
