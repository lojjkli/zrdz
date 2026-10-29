import {Cam, clamp01, shake, V3} from '../three/cam';

export type Shot = {from: number; to: number; cam: (t: number, k: number) => Cam};

export const shotAt = (shots: Shot[], t: number) => {
	const i = Math.max(0, shots.findIndex((s) => t >= s.from && t < s.to));
	const s = shots.find((x) => t >= x.from && t < x.to) ?? shots[shots.length - 1];
	return {cam: s.cam(t, clamp01((t - s.from) / (s.to - s.from))), i, from: s.from};
};

export const withShake = (cam: Cam, t: number, amt: number): Cam => {
	if (amt <= 0) return cam;
	const s = shake(t, amt);
	return {...cam, pos: [cam.pos[0] + s[0], cam.pos[1] + s[1], cam.pos[2] + s[2]] as V3, roll: (cam.roll ?? 0) + s[2] * 0.05};
};

export const add = (a: V3, b: V3): V3 => [a[0] + b[0], a[1] + b[1], a[2] + b[2]];

/** yaw so that an avatar at `from` faces `to` (avatars face +z at yaw 0) */
export const face = (from: V3, to: V3) => Math.atan2(to[0] - from[0], to[2] - from[2]);
