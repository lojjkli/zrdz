import voices from './voices.json';

export const FPS = 30;
export const W = 1920;
export const H = 1080;
export const f = (sec: number) => Math.round(sec * FPS);

// Scene boundaries in seconds.
export const SCENES = {
	cold: [0, 8],
	peace: [8, 22],
	reveal: [22, 38],
	sun: [38, 52],
	plan: [52, 64],
	blender: [64, 81],
	bait: [81, 99],
	sunback: [99, 108],
	pet: [108, 124],
	end: [124, 136],
} as const;

export const TOTAL = f(SCENES.end[1]);

export type VoiceId = keyof typeof voices;
export type Speaker = 'narr' | 'kli' | 'myninn' | 'donut' | 'pigeon' | 'cube' | 'crowd' | 'sfx';

export const speakerOf = (id: VoiceId): Speaker =>
	(({n: 'narr', k: 'kli', m: 'myninn', d: 'donut', p: 'pigeon', q: 'cube', c: 'crowd', s: 'sfx'}) as Record<string, Speaker>)[id[0]] ?? 'sfx';

export const SPEAKER_TAG: Record<Speaker, [string, string] | null> = {
	narr: null,
	sfx: null,
	crowd: ['Everyone', '#ffb3b3'],
	kli: ['kli', '#b9b9ff'],
	myninn: ['myninn', '#5fe3d2'],
	donut: ['TheDonut', '#ff8fc8'],
	pigeon: ['THE PIGEON', '#a9b4c4'],
	cube: ['Cube', '#ffa21a'],
};

export const SUN_GRAB = 40.0;
export const SUN_BACK = 100.2;
export const RENDER_FAST = 78.0;

export const VOICE_CUES: {id: VoiceId; at: number; vol?: number}[] = [
	{id: 'n_prev', at: 0.8},
	{id: 'n_peace', at: 8.6},
	{id: 'd_tea', at: 13.2},
	{id: 'k_yes', at: 15.2},
	{id: 'n_but', at: 17.6},
	{id: 'p_coo', at: 22.6},
	{id: 'n_pigeon', at: 24.6},
	{id: 'n_huge', at: 29.0},
	{id: 'p_bread', at: 32.2},
	{id: 'n_sun', at: 38.6},
	{id: 'k_sun', at: 43.2},
	{id: 'm_how', at: 46.2},
	{id: 'c_dark', at: 48.8, vol: 0.9},
	{id: 'n_team', at: 52.6},
	{id: 'd_idea', at: 56.6},
	{id: 'k_blender', at: 59.4},
	{id: 'n_model', at: 64.6},
	{id: 'k_render', at: 68.2},
	{id: 'n_render', at: 71.8},
	{id: 'm_440', at: 75.2},
	{id: 'n_bait', at: 81.6},
	{id: 'p_mine', at: 87.0},
	{id: 'n_ate', at: 91.8},
	{id: 'k_now', at: 96.0},
	{id: 'n_back', at: 99.6},
	{id: 'c_yay', at: 103.0, vol: 0.9},
	{id: 'p_sorry', at: 110.4},
	{id: 'k_share', at: 115.2},
	{id: 'n_pet', at: 120.2},
	{id: 'n_end', at: 126.0},
	{id: 'q_deleted', at: 132.0},
	{id: 'k_ohno', at: 134.0},
];

export const voiceSec = (id: VoiceId) => voices[id].sec;
export const voiceText = (id: VoiceId) => voices[id].text;
export const voiceFile = (id: VoiceId) => voices[id].file;

export const talking = (who: Speaker, t: number) =>
	VOICE_CUES.some((c) => speakerOf(c.id) === who && t >= c.at && t <= c.at + voiceSec(c.id) - 0.05);

export type Sfx =
	| 'tap' | 'pop' | 'chat' | 'whoosh' | 'sparkle' | 'cheer' | 'rumble' | 'boom' | 'crack' | 'siren'
	| 'disconnect' | 'braam' | 'riser' | 'scratch' | 'land' | 'heartpop' | 'steps' | 'fart' | 'vineboom'
	| 'role' | 'join' | 'leave' | 'door' | 'gas' | 'choir' | 'heartbeat' | 'rain' | 'freeze' | 'bigboom'
	| 'purchase' | 'win' | 'lose' | 'diamond' | 'buzz' | 'bells' | 'meteor' | 'reel';

export const TAPS: [number, number, number][] = [];

export const SFX_CUES: {id: Sfx; at: number; vol?: number; dur?: number}[] = [
	{id: 'braam', at: 0.2, vol: 0.5},
	{id: 'riser', at: 3.2, vol: 0.35},
	{id: 'vineboom', at: 4.4, vol: 0.7},
	// peace
	{id: 'bells', at: 13.0, vol: 0.35},
	{id: 'riser', at: 17.4, vol: 0.3},
	// reveal
	{id: 'vineboom', at: 22.6, vol: 0.6},
	{id: 'scratch', at: 28.9, vol: 0.5},
	{id: 'bigboom', at: 30.4, vol: 0.7},
	{id: 'vineboom', at: 30.4, vol: 0.9},
	{id: 'rumble', at: 32.2, vol: 0.7},
	{id: 'whoosh', at: 35.8, vol: 0.6},
	// sun
	{id: 'whoosh', at: 38.8, vol: 0.6},
	{id: 'whoosh', at: SUN_GRAB, vol: 0.7},
	{id: 'lose', at: SUN_GRAB + 0.3, vol: 0.5},
	{id: 'rumble', at: SUN_GRAB + 0.5, vol: 0.5},
	{id: 'chat', at: 48.0, vol: 0.3},
	{id: 'chat', at: 49.4, vol: 0.3},
	{id: 'chat', at: 50.2, vol: 0.3},
	// plan
	{id: 'sparkle', at: 56.6, vol: 0.5},
	{id: 'pop', at: 56.7, vol: 0.4},
	// blender
	{id: 'pop', at: 65.6, vol: 0.5},
	{id: 'tap', at: 68.0, vol: 0.5},
	{id: 'buzz', at: 72.6, vol: 0.4},
	{id: 'scratch', at: 77.9, vol: 0.5},
	{id: 'riser', at: RENDER_FAST - 0.2, vol: 0.4},
	{id: 'win', at: RENDER_FAST + 1.2, vol: 0.5},
	// bait
	{id: 'whoosh', at: 84.8, vol: 0.6},
	{id: 'land', at: 86.6, vol: 0.9},
	{id: 'rumble', at: 86.7, vol: 0.5},
	...new Array(6).fill(0).map((_, i) => ({id: 'pop' as Sfx, at: 89.6 + i * 0.35, vol: 0.55})),
	{id: 'heartbeat', at: 93.0, vol: 0.35},
	{id: 'vineboom', at: 96.0, vol: 0.6},
	// sun back
	{id: 'riser', at: 99.4, vol: 0.4},
	{id: 'choir', at: SUN_BACK + 1.0, vol: 0.55},
	{id: 'cheer', at: 103.0, vol: 0.45},
	{id: 'chat', at: 103.4, vol: 0.3},
	{id: 'chat', at: 104.0, vol: 0.3},
	// pet
	{id: 'whoosh', at: 108.6, vol: 0.4},
	{id: 'pop', at: 110.0, vol: 0.5},
	{id: 'sparkle', at: 116.6, vol: 0.4},
	{id: 'whoosh', at: 119.0, vol: 0.4},
	{id: 'heartpop', at: 119.9, vol: 0.5},
	// end
	{id: 'braam', at: 124.2, vol: 0.6},
	{id: 'pop', at: 131.0, vol: 0.5},
	{id: 'scratch', at: 133.6, vol: 0.4},
	{id: 'vineboom', at: 134.0, vol: 0.8},
];

export const MUSIC_CUES: {id: string; from: number; to: number; vol: number; fadeIn?: number; fadeOut?: number; offset?: number}[] = [
	{id: 'intro', from: 0, to: 8.2, vol: 0.5, fadeOut: 0.8},
	{id: 'romance', from: 8.2, to: 17.4, vol: 0.26, fadeIn: 0.8, fadeOut: 0.6, offset: 2},
	{id: 'mystery', from: 17.4, to: 30.3, vol: 0.32, fadeIn: 0.5, fadeOut: 0.05},
	{id: 'chaos', from: 30.4, to: 42.5, vol: 0.34, fadeIn: 0.05, fadeOut: 0.8},
	{id: 'sad', from: 42.6, to: 63.6, vol: 0.26, fadeIn: 0.8, fadeOut: 0.6, offset: 4},
	{id: 'party', from: 64.0, to: 77.9, vol: 0.28, fadeIn: 0.4, fadeOut: 0.05},
	{id: 'party', from: 78.2, to: 80.8, vol: 0.34, fadeIn: 0.05, fadeOut: 0.5, offset: 8},
	{id: 'mystery', from: 81.2, to: 98.8, vol: 0.28, fadeIn: 0.6, fadeOut: 0.6, offset: 6},
	{id: 'party', from: 99.4, to: 107.8, vol: 0.32, fadeIn: 0.6, fadeOut: 0.6},
	{id: 'romance', from: 108.2, to: 123.8, vol: 0.3, fadeIn: 0.8, fadeOut: 0.8, offset: 6},
	{id: 'intro', from: 124.0, to: 130.0, vol: 0.45, fadeIn: 0.2, fadeOut: 1.0, offset: 3},
];

export type ChatLine = {at: number; name: string; text: string; color?: string; system?: boolean};

export const C = {
	kli: '#c7c7ff',
	myninn: '#5fe3d2',
	donut: '#ff8fc8',
	toast: '#ffd166',
	slasher: '#ff7a7a',
	lily: '#ff9ad5',
	kaiib: '#9cff8a',
};

export const HATERS = [
	{name: 'Toast_YT', color: C.toast},
	{name: 'xXslasherXx', color: C.slasher},
	{name: 'Lilyy_bloom', color: C.lily},
	{name: 'kaiib', color: C.kaiib},
];

export const CHAT: ChatLine[] = [
	{at: 48.0, name: 'Toast_YT', text: 'WHO TOOK THE SUN', color: C.toast},
	{at: 49.4, name: 'Lilyy_bloom', text: 'i cant see my avatar 😭', color: C.lily},
	{at: 50.2, name: 'kaiib', text: 'the pigeon did it fr', color: C.kaiib},
	{at: 103.4, name: 'Toast_YT', text: 'SUN IS BACK 🌞', color: C.toast},
	{at: 104.0, name: 'xXslasherXx', text: 'kli saved roblox again', color: C.slasher},
	{at: 121.0, name: 'Lilyy_bloom', text: 'the pigeon is so cute now 🥹', color: C.lily},
];

export const bubbleOf = (name: string, t: number) => {
	const b = [...CHAT].reverse().find((c) => c.name === name && t >= c.at && t < c.at + 2.6);
	return b ? {text: b.text, age: t - b.at} : null;
};
