import voices from './voices.json';

export const FPS = 30;
export const W = 1920;
export const H = 1080;
export const f = (sec: number) => Math.round(sec * FPS);

// Scene boundaries in seconds.
export const SCENES = {
	cold: [0, 9],
	box: [9, 24],
	throne: [24, 46],
	plan: [46, 54],
	blender: [54, 66],
	battle: [66, 94],
	butler: [94, 106],
	end: [106, 120],
} as const;

export const TOTAL = f(SCENES.end[1]);

export type VoiceId = keyof typeof voices;
export type Speaker = 'narr' | 'kli' | 'myninn' | 'donut' | 'crowd' | 'sfx';

export const speakerOf = (id: VoiceId): Speaker =>
	(({n: 'narr', k: 'kli', m: 'myninn', d: 'donut', c: 'crowd', s: 'sfx'}) as Record<string, Speaker>)[id[0]] ?? 'sfx';

export const SPEAKER_TAG: Record<Speaker, [string, string] | null> = {
	narr: null,
	sfx: null,
	crowd: ['Everyone', '#ffb3b3'],
	kli: ['kli', '#b9b9ff'],
	myninn: ['myninn', '#5fe3d2'],
	donut: ['TheDonut', '#ff8fc8'],
};

// the donut steals kli's deep voice, then gives it back
export const ZAP = 38.2;
export const GIFT = 90.0;
export const STAB = 75.2;

export const VOICE_CUES: {id: VoiceId; at: number; vol?: number}[] = [
	{id: 'n_prev', at: 0.8},
	{id: 'n_woke', at: 9.6},
	{id: 'k_robux', at: 13.2},
	{id: 'm_gone', at: 16.0},
	{id: 'k_donut', at: 18.6},
	{id: 'n_ceo', at: 24.6},
	{id: 'c_hail', at: 28.6, vol: 0.9},
	{id: 'd_kli', at: 30.4},
	{id: 'd_rule', at: 34.6},
	{id: 'k_ohno', at: 39.8},
	{id: 'c_laugh', at: 41.4, vol: 0.85},
	{id: 'n_plan', at: 46.6},
	{id: 'm_fork', at: 49.2},
	{id: 'k_fork', at: 51.6},
	{id: 'n_built', at: 54.4},
	{id: 'n_hours', at: 59.2},
	{id: 'k_done', at: 64.0},
	{id: 'n_battle', at: 66.6},
	{id: 'd_laugh', at: 69.2},
	{id: 'k_charge', at: 73.0},
	{id: 'd_ow', at: 75.6},
	{id: 'd_cry', at: 78.4},
	{id: 'k_hug', at: 81.8},
	{id: 'n_friends', at: 83.6},
	{id: 'd_gift', at: 87.4},
	{id: 'k_back', at: 90.6},
	{id: 'n_butler', at: 94.6},
	{id: 'd_tea', at: 98.4},
	{id: 'k_nice', at: 100.6},
	{id: 'n_part3', at: 108.4},
	{id: 'k_post', at: 113.8},
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
	{id: 'rumble', at: 2.6, vol: 0.5},
	{id: 'riser', at: 3.6, vol: 0.35},
	{id: 'vineboom', at: 5.2, vol: 0.8},
	// box
	{id: 'buzz', at: 13.4, vol: 0.4},
	{id: 'steps', at: 14.0, vol: 0.3},
	{id: 'scratch', at: 18.5, vol: 0.5},
	{id: 'vineboom', at: 18.7, vol: 0.7},
	// throne
	{id: 'choir', at: 24.4, vol: 0.5},
	{id: 'bells', at: 25.6, vol: 0.4},
	{id: 'chat', at: 28.8, vol: 0.3},
	{id: 'chat', at: 29.2, vol: 0.3},
	{id: 'riser', at: 36.6, vol: 0.45},
	{id: 'boom', at: ZAP, vol: 0.9},
	{id: 'whoosh', at: ZAP + 0.1, vol: 0.5},
	{id: 'pop', at: ZAP + 1.2, vol: 0.5},
	{id: 'scratch', at: 39.7, vol: 0.5},
	{id: 'chat', at: 41.6, vol: 0.3},
	{id: 'chat', at: 42.2, vol: 0.3},
	// plan
	{id: 'sparkle', at: 51.6, vol: 0.5},
	{id: 'vineboom', at: 51.65, vol: 0.7},
	// blender
	{id: 'tap', at: 55.2, vol: 0.5},
	{id: 'pop', at: 55.4, vol: 0.5},
	{id: 'riser', at: 56.0, vol: 0.3},
	{id: 'pop', at: 59.6, vol: 0.5},
	{id: 'pop', at: 61.6, vol: 0.5},
	...new Array(8).fill(0).map((_, i) => ({id: 'land' as Sfx, at: 60.0 + i * 0.4, vol: 0.25})),
	{id: 'choir', at: 63.8, vol: 0.5},
	{id: 'sparkle', at: 64.0, vol: 0.5},
	// battle
	{id: 'braam', at: 66.4, vol: 0.5},
	{id: 'steps', at: 73.2, vol: 0.5},
	{id: 'riser', at: 73.4, vol: 0.4},
	{id: 'boom', at: STAB, vol: 1.0},
	{id: 'crack', at: STAB, vol: 0.7},
	{id: 'chat', at: 75.6, vol: 0.3},
	{id: 'scratch', at: 78.2, vol: 0.4},
	{id: 'chat', at: 79.0, vol: 0.3},
	{id: 'heartbeat', at: 82.6, vol: 0.7},
	{id: 'heartpop', at: 83.0, vol: 0.5},
	{id: 'chat', at: 84.0, vol: 0.3},
	{id: 'riser', at: 88.6, vol: 0.4},
	{id: 'boom', at: GIFT, vol: 0.8},
	{id: 'vineboom', at: 90.6, vol: 0.8},
	// butler
	{id: 'bells', at: 98.2, vol: 0.4},
	{id: 'chat', at: 99.0, vol: 0.3},
	{id: 'chat', at: 99.8, vol: 0.3},
	{id: 'vineboom', at: 100.6, vol: 0.7},
	{id: 'cheer', at: 102.0, vol: 0.35},
	// end
	{id: 'braam', at: 106.2, vol: 0.6},
	{id: 'scratch', at: 116.8, vol: 0.4},
	{id: 'whoosh', at: 117.0, vol: 0.6},
	{id: 'vineboom', at: 118.6, vol: 0.6},
];

export const MUSIC_CUES: {id: string; from: number; to: number; vol: number; fadeIn?: number; fadeOut?: number; offset?: number}[] = [
	{id: 'intro', from: 0, to: 9.2, vol: 0.5, fadeOut: 0.8},
	{id: 'sad', from: 9.2, to: 18.5, vol: 0.3, fadeIn: 0.8, fadeOut: 0.05, offset: 3},
	{id: 'mystery', from: 24.0, to: 39.7, vol: 0.3, fadeIn: 0.6, fadeOut: 0.05},
	{id: 'lobby', from: 41.2, to: 45.8, vol: 0.2, fadeIn: 0.3, fadeOut: 0.5},
	{id: 'sad', from: 46.0, to: 51.5, vol: 0.28, fadeIn: 0.6, fadeOut: 0.05, offset: 8},
	{id: 'party', from: 54.0, to: 65.8, vol: 0.3, fadeIn: 0.3, fadeOut: 0.6},
	{id: 'chaos', from: 66.4, to: 78.2, vol: 0.34, fadeIn: 0.3, fadeOut: 0.05},
	{id: 'sad', from: 78.4, to: 82.6, vol: 0.3, fadeIn: 0.4, fadeOut: 0.5},
	{id: 'romance', from: 82.6, to: 93.8, vol: 0.32, fadeIn: 0.8, fadeOut: 0.6},
	{id: 'party', from: 94.0, to: 105.8, vol: 0.28, fadeIn: 0.4, fadeOut: 0.8, offset: 6},
	{id: 'intro', from: 106.0, to: 112.2, vol: 0.45, fadeIn: 0.2, fadeOut: 1.0, offset: 3},
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
	{at: 24.8, name: '', text: 'TheDonut is now the owner of this experience.', system: true},
	{at: 28.8, name: 'Toast_YT', text: 'ALL HAIL DONUT 🍩', color: C.toast},
	{at: 29.2, name: 'Lilyy_bloom', text: '🍩🍩🍩🍩', color: C.lily},
	{at: 41.6, name: 'xXslasherXx', text: 'SQUEAKY KLI IS BACK 💀', color: C.slasher},
	{at: 42.2, name: 'Toast_YT', text: '😭😭😭', color: C.toast},
	{at: 75.6, name: 'kaiib', text: 'HE ACTUALLY DID IT', color: C.kaiib},
	{at: 79.0, name: 'Lilyy_bloom', text: 'wait why am i crying', color: C.lily},
	{at: 84.0, name: 'Toast_YT', text: 'best duo ever 🥹', color: C.toast},
	{at: 99.0, name: 'myninn', text: 'can i get tea too', color: C.myninn},
	{at: 99.8, name: 'TheDonut', text: 'no.', color: C.donut},
];

export const bubbleOf = (name: string, t: number) => {
	const b = [...CHAT].reverse().find((c) => c.name === name && t >= c.at && t < c.at + 2.6);
	return b ? {text: b.text, age: t - b.at} : null;
};
