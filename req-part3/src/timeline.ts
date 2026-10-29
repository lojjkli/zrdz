import voices from './voices.json';

export const FPS = 30;
export const W = 1920;
export const H = 1080;
export const f = (sec: number) => Math.round(sec * FPS);

// Scene boundaries in seconds.
export const SCENES = {
	cold: [0, 9],
	night: [9, 24.6],
	inside: [24.6, 50.6],
	run: [50.6, 58.4],
	outside: [58.4, 66.4],
	out: [66.4, 81],
	end: [81, 93],
} as const;

export const TOTAL = f(SCENES.end[1]);

export type VoiceId = keyof typeof voices;
export type Speaker = 'narr' | 'req' | 'kli' | 'machine' | 'pigeon' | 'hamster' | 'crowd' | 'sfx';

export const speakerOf = (id: VoiceId): Speaker =>
	(({n: 'narr', r: 'req', k: 'kli', v: 'machine', p: 'pigeon', h: 'hamster', c: 'crowd', s: 'sfx'}) as Record<string, Speaker>)[id[0]] ?? 'sfx';

export const SPEAKER_TAG: Record<Speaker, [string, string] | null> = {
	narr: null,
	sfx: null,
	crowd: ['Everyone', '#ffb3b3'],
	req: ['REQ', '#ff5b5b'],
	kli: ['lojjkli', '#b9b9ff'],
	machine: ['LUCKY SPIN', '#ff5bd6'],
	pigeon: ['THE PIGEON', '#a9b4c4'],
	hamster: ['Hamster', '#ffb36b'],
};

export const SUCK = 19.8;
export const CURTAIN = 39.2;
export const WHEEL = 53.2;
export const PECK = 65.6;
export const POP = 66.4;

export const VOICE_CUES: {id: VoiceId; at: number; vol?: number}[] = [
	{id: 'n_prev', at: 0.6},
	{id: 'n_night', at: 9.6},
	{id: 'r_one', at: 13.2},
	{id: 'v_closer', at: 16.2},
	{id: 'r_closer', at: 18.6},
	{id: 'n_pulled', at: 21.4},
	{id: 'r_where', at: 25.4},
	{id: 'n_inside', at: 27.0},
	{id: 'v_welcome', at: 30.2},
	{id: 'r_alot', at: 34.8},
	{id: 'n_curtain', at: 36.6},
	{id: 'n_hamster', at: 40.4},
	{id: 'h_tired', at: 44.4},
	{id: 'r_you', at: 46.2},
	{id: 'h_every', at: 48.2},
	{id: 'r_break', at: 51.0},
	{id: 'n_run', at: 53.6},
	{id: 'k_scream', at: 58.8},
	{id: 'p_coo', at: 62.4},
	{id: 'n_peck', at: 63.6},
	{id: 'h_free', at: 67.0},
	{id: 'r_hard', at: 69.0},
	{id: 'h_cardio', at: 71.6},
	{id: 'n_quit', at: 73.6},
	{id: 'r_probably', at: 78.2},
	{id: 'n_end', at: 82.6},
	{id: 'h_best', at: 88.8},
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
	| 'tinyfart' | 'purchase' | 'win' | 'lose' | 'diamond' | 'buzz' | 'bells' | 'meteor' | 'reel';

export const TAPS: [number, number, number][] = [];

export const SFX_CUES: {id: Sfx; at: number; vol?: number; dur?: number}[] = [
	{id: 'braam', at: 0.2, vol: 0.5},
	{id: 'riser', at: 3.2, vol: 0.35},
	{id: 'vineboom', at: 4.4, vol: 0.7},
	// night
	{id: 'sparkle', at: 16.2, vol: 0.5},
	{id: 'heartbeat', at: 17.8, vol: 0.4},
	{id: 'riser', at: SUCK - 0.6, vol: 0.5},
	{id: 'whoosh', at: SUCK, vol: 0.8},
	{id: 'whoosh', at: SUCK + 0.6, vol: 0.6},
	{id: 'pop', at: SUCK + 1.4, vol: 0.6},
	// inside
	{id: 'land', at: 24.9, vol: 0.6},
	{id: 'braam', at: 30.0, vol: 0.4},
	{id: 'door', at: CURTAIN, vol: 0.5},
	{id: 'vineboom', at: 42.4, vol: 0.7},
	{id: 'heartpop', at: 44.4, vol: 0.3},
	// run
	{id: 'whoosh', at: WHEEL - 0.2, vol: 0.5},
	{id: 'steps', at: WHEEL + 0.4, vol: 0.5},
	{id: 'reel', at: 54.0, vol: 0.4},
	{id: 'reel', at: 55.8, vol: 0.4},
	{id: 'siren', at: 56.8, vol: 0.25, dur: 1.6},
	// outside
	{id: 'rumble', at: 58.4, vol: 0.5},
	{id: 'chat', at: 60.4, vol: 0.3},
	{id: 'tap', at: PECK, vol: 0.9},
	{id: 'bigboom', at: POP - 0.1, vol: 0.5},
	// out
	{id: 'pop', at: POP, vol: 0.7},
	{id: 'cheer', at: 67.0, vol: 0.4},
	{id: 'choir', at: 73.6, vol: 0.3},
	{id: 'scratch', at: 78.0, vol: 0.4},
	{id: 'vineboom', at: 78.3, vol: 0.5},
	// end
	{id: 'braam', at: 81.2, vol: 0.6},
	{id: 'sparkle', at: 88.6, vol: 0.4},
];

export const MUSIC_CUES: {id: string; from: number; to: number; vol: number; fadeIn?: number; fadeOut?: number; offset?: number}[] = [
	{id: 'intro', from: 0, to: 9.2, vol: 0.5, fadeOut: 0.8},
	{id: 'mystery', from: 9.2, to: 24.4, vol: 0.3, fadeIn: 0.5, fadeOut: 0.3},
	{id: 'chaos', from: 24.6, to: 39.0, vol: 0.26, fadeIn: 0.4, fadeOut: 0.2},
	{id: 'sad', from: 39.6, to: 50.4, vol: 0.28, fadeIn: 0.6, fadeOut: 0.4},
	{id: 'chaos', from: 50.6, to: 66.2, vol: 0.32, fadeIn: 0.2, fadeOut: 0.2, offset: 6},
	{id: 'party', from: POP, to: 80.8, vol: 0.3, fadeIn: 0.1, fadeOut: 0.6},
	{id: 'intro', from: 81.0, to: 86.8, vol: 0.45, fadeIn: 0.2, fadeOut: 1.0, offset: 3},
	{id: 'romance', from: 87.2, to: 93, vol: 0.26, fadeIn: 0.5, fadeOut: 0.6, offset: 3},
];

export type ChatLine = {at: number; name: string; text: string; color?: string; system?: boolean};

export const CHAT: ChatLine[] = [
	{at: 60.4, name: 'GamingSquirrel39', text: 'the slot machine is yelling 💀', color: '#ffd166'},
	{at: 68.0, name: 'kaiib', text: 'FREE THE HAMSTER', color: '#9cff8a'},
	{at: 78.6, name: 'lewlone', text: 'probably 💀💀', color: '#7ad1ff'},
];

export const bubbleOf = (name: string, t: number) => {
	const b = [...CHAT].reverse().find((c) => c.name === name && t >= c.at && t < c.at + 2.6);
	return b ? {text: b.text, age: t - b.at} : null;
};
