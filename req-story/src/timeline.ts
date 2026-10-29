import voices from './voices.json';

export const FPS = 30;
export const W = 1920;
export const H = 1080;
export const f = (sec: number) => Math.round(sec * FPS);

// Scene boundaries in seconds.
export const SCENES = {
	cold: [0, 7],
	app: [7, 14.5],
	spawn: [14.5, 23],
	machine: [23, 48],
	sad: [48, 56],
	arrival: [56, 64.5],
	wedding: [64.5, 77.5],
	collapse: [77.5, 89],
	disconnect: [89, 93],
	end: [93, 102],
} as const;

export const TOTAL = f(SCENES.end[1]);

export type VoiceId = keyof typeof voices;
export type Speaker = 'narr' | 'req' | 'crowd';

export const speakerOf = (id: VoiceId): Speaker =>
	id.startsWith('n_') ? 'narr' : id.startsWith('r_') ? 'req' : 'crowd';

export const VOICE_CUES: {id: VoiceId; at: number; vol?: number}[] = [
	{id: 'n_intro', at: 1.0},
	{id: 'n_problem', at: 3.0},
	{id: 'n_found', at: 7.6},
	{id: 'n_had', at: 15.2},
	{id: 'r_fire', at: 19.6},
	{id: 'n_machine', at: 23.4},
	{id: 'r_onespin', at: 25.8},
	{id: 'r_onemore1', at: 30.6},
	{id: 'n_everyday', at: 33.4},
	{id: 'r_onemore2', at: 37.2},
	{id: 'r_onemore3', at: 38.6},
	{id: 'r_99', at: 40.0},
	{id: 'n_gone', at: 48.6},
	{id: 'r_onemore_sad', at: 54.6},
	{id: 'n_flying', at: 56.8},
	{id: 'r_woah', at: 60.6},
	{id: 'n_wedding', at: 65.0},
	{id: 'r_ido', at: 70.6},
	{id: 'c_letsgo', at: 71.6, vol: 0.7},
	{id: 'c_w', at: 72.3, vol: 0.6},
	{id: 'r_after', at: 73.6},
	{id: 'n_perfect', at: 76.0},
	{id: 'r_sky', at: 78.0},
	{id: 'n_collapse', at: 79.8},
	{id: 's_aah1', at: 82.4, vol: 0.55},
	{id: 's_aah2', at: 82.9, vol: 0.5},
	{id: 'r_run', at: 83.3},
	{id: 's_noo', at: 84.3, vol: 0.5},
	{id: 's_run', at: 84.8, vol: 0.5},
	{id: 'r_pets', at: 85.6},
	{id: 's_oof', at: 87.0, vol: 0.6},
	{id: 'n_soon', at: 94.6},
	{id: 'r_whisper', at: 99.0, vol: 0.8},
];

export const voiceSec = (id: VoiceId) => voices[id].sec;
export const voiceText = (id: VoiceId) => voices[id].text;
export const voiceFile = (id: VoiceId) => voices[id].file;

// Is REQ talking on voice chat at time t (sec)? Used for the mic indicator.
export const reqTalking = (t: number) =>
	VOICE_CUES.some(
		(c) => speakerOf(c.id) === 'req' && t >= c.at && t <= c.at + voiceSec(c.id) - 0.05,
	);

export type Sfx =
	| 'tap' | 'pop' | 'chat' | 'diamond' | 'reel' | 'lose' | 'buzz' | 'win' | 'purchase' | 'whoosh'
	| 'sparkle' | 'bells' | 'cheer' | 'rumble' | 'boom' | 'crack' | 'siren' | 'meteor' | 'disconnect'
	| 'braam' | 'riser' | 'scratch' | 'land' | 'heartpop' | 'steps';

// Taps on the screen (also drive the touch indicator): [sec, x, y]
export const TAPS: [number, number, number][] = [
	[8.9, 474, 342], // PS99 tile on home
	[11.2, 1460, 610], // Play button
	[27.4, 960, 880], // spin
	[31.5, 960, 880],
	[34.3, 960, 880],
	[35.3, 960, 880],
	[36.3, 960, 880],
	[38.2, 960, 880],
	[39.8, 960, 880],
	[44.9, 1150, 700], // buy
	[45.4, 960, 880],
	[55.5, 960, 880], // not enough diamonds
];

export const SFX_CUES: {id: Sfx; at: number; vol?: number; dur?: number}[] = [
	// cold open
	{id: 'braam', at: 0.2, vol: 0.55},
	{id: 'riser', at: 4.2, vol: 0.4},
	// app
	...TAPS.map(([at]) => ({id: 'tap' as Sfx, at, vol: 0.6})),
	{id: 'pop', at: 9.0, vol: 0.4},
	{id: 'pop', at: 11.3, vol: 0.4},
	// spawn: diamond pickups
	{id: 'diamond', at: 16.2, vol: 0.45},
	{id: 'diamond', at: 17.4, vol: 0.45},
	{id: 'diamond', at: 18.7, vol: 0.45},
	{id: 'diamond', at: 20.3, vol: 0.45},
	{id: 'steps', at: 15.0, vol: 0.35},
	{id: 'steps', at: 19.0, vol: 0.35},
	// machine
	{id: 'riser', at: 21.0, vol: 0.35},
	{id: 'win', at: 23.1, vol: 0.4},
	{id: 'pop', at: 26.9, vol: 0.4},
	{id: 'reel', at: 27.5, vol: 0.9},
	{id: 'lose', at: 29.4, vol: 0.45},
	{id: 'reel', at: 31.6, vol: 0.9},
	{id: 'buzz', at: 33.1, vol: 0.25},
	{id: 'reel', at: 34.35, vol: 0.7, dur: 0.8},
	{id: 'buzz', at: 35.1, vol: 0.2},
	{id: 'reel', at: 35.35, vol: 0.7, dur: 0.8},
	{id: 'buzz', at: 36.1, vol: 0.2},
	{id: 'reel', at: 36.35, vol: 0.7, dur: 0.8},
	{id: 'buzz', at: 37.1, vol: 0.2},
	{id: 'reel', at: 38.3, vol: 0.7, dur: 1.2},
	{id: 'buzz', at: 39.5, vol: 0.2},
	{id: 'reel', at: 39.9, vol: 0.7, dur: 1.2},
	{id: 'buzz', at: 41.1, vol: 0.2},
	{id: 'pop', at: 43.8, vol: 0.5},
	{id: 'purchase', at: 45.0, vol: 0.6},
	{id: 'reel', at: 45.5, vol: 0.9},
	{id: 'lose', at: 47.0, vol: 0.5},
	// sad
	{id: 'buzz', at: 55.6, vol: 0.3},
	// arrival
	{id: 'sparkle', at: 56.3, vol: 0.4},
	{id: 'whoosh', at: 58.0, vol: 0.8},
	{id: 'whoosh', at: 59.0, vol: 0.6},
	{id: 'land', at: 60.0, vol: 0.7},
	{id: 'sparkle', at: 60.0, vol: 0.5},
	{id: 'heartpop', at: 60.1, vol: 0.4},
	{id: 'pop', at: 62.0, vol: 0.3},
	{id: 'pop', at: 63.2, vol: 0.3},
	// wedding
	{id: 'bells', at: 64.5, vol: 0.5},
	{id: 'pop', at: 69.0, vol: 0.3},
	{id: 'cheer', at: 71.2, vol: 0.55},
	{id: 'heartpop', at: 71.2, vol: 0.45},
	{id: 'scratch', at: 73.2, vol: 0.6},
	{id: 'pop', at: 75.2, vol: 0.3},
	// collapse
	{id: 'rumble', at: 77.4, vol: 0.8},
	{id: 'boom', at: 82.0, vol: 0.9},
	{id: 'crack', at: 82.1, vol: 0.8},
	{id: 'rumble', at: 82.0, vol: 0.9},
	{id: 'siren', at: 82.2, vol: 0.12, dur: 6.5},
	{id: 'steps', at: 82.6, vol: 0.4},
	{id: 'steps', at: 86.5, vol: 0.4},
	{id: 'meteor', at: 84.6, vol: 0.5},
	{id: 'crack', at: 85.4, vol: 0.6},
	{id: 'meteor', at: 86.2, vol: 0.5},
	{id: 'boom', at: 86.8, vol: 0.45},
	{id: 'meteor', at: 87.4, vol: 0.6},
	{id: 'boom', at: 88.6, vol: 1},
	// disconnect + end
	{id: 'disconnect', at: 89.2, vol: 0.5},
	{id: 'braam', at: 93.2, vol: 0.7},
	{id: 'reel', at: 100.0, vol: 0.6, dur: 1.0},
];

export const MUSIC_CUES: {id: string; from: number; to: number; vol: number; fadeIn?: number; fadeOut?: number; offset?: number}[] = [
	{id: 'intro', from: 0, to: 7.4, vol: 0.5, fadeOut: 0.8},
	{id: 'lobby', from: 7.0, to: 23.4, vol: 0.32, fadeIn: 0.4, fadeOut: 0.8},
	{id: 'casino', from: 23.0, to: 47.6, vol: 0.3, fadeIn: 0.2, fadeOut: 0.6},
	{id: 'sad', from: 47.6, to: 56.4, vol: 0.45, fadeIn: 0.5, fadeOut: 1.0},
	{id: 'wedding', from: 56.0, to: 64.5, vol: 0.3, fadeIn: 2.0, fadeOut: 0.3},
	{id: 'wedding', from: 64.5, to: 73.25, vol: 0.4, fadeIn: 0.1, fadeOut: 0.05, offset: 0},
	{id: 'wedding', from: 75.8, to: 77.8, vol: 0.25, fadeIn: 0.5, fadeOut: 0.6, offset: 11.5},
	{id: 'chaos', from: 82.0, to: 88.65, vol: 0.45, fadeIn: 0.05, fadeOut: 0.05},
	{id: 'intro', from: 93.0, to: 98.5, vol: 0.45, fadeIn: 0.2, fadeOut: 1.5, offset: 3.0},
];

// Diamonds over time (sec) for the HUD. Step changes are animated by the HUD.
export const DIAMONDS: [number, number][] = [
	[0, 1250000],
	[16.2, 1262500],
	[17.4, 1270000],
	[18.7, 1279000],
	[20.3, 1284500],
	[27.4, 1034500],
	[31.5, 784500],
	[34.3, 412000],
	[35.3, 96000],
	[36.3, 18500],
	[38.2, 3500],
	[39.8, 0],
	[45.0, 250000],
	[45.4, 0],
];

export const diamondsAt = (t: number) => {
	let v = DIAMONDS[0][1];
	let prev = v;
	let changedAt = -99;
	for (const [at, val] of DIAMONDS) {
		if (t >= at) {
			prev = v;
			v = val;
			changedAt = at;
		}
	}
	// count animation over 0.6s
	const k = Math.min(1, (t - changedAt) / 0.6);
	const e = 1 - Math.pow(1 - k, 3);
	return {value: Math.round(prev + (v - prev) * e), changedAt, delta: v - prev};
};

export type ChatLine = {at: number; name: string; text: string; color?: string; system?: boolean};

export const CHAT: ChatLine[] = [
	{at: 14.8, name: '', text: 'REQ has joined the experience.', system: true},
	{at: 16.0, name: 'Emii5287', text: 'anyone trading huges?', color: '#ff7ab6'},
	{at: 18.0, name: 'kaiib', text: 'nice pets REQ', color: '#7ad3ff'},
	{at: 21.5, name: 'HachiMC', text: 'whats the machine for', color: '#ffd166'},
	{at: 29.6, name: 'HachiMC', text: 'unlucky 💀', color: '#ffd166'},
	{at: 33.8, name: 'GamingSquirrel39', text: 'bro stop', color: '#9cff8a'},
	{at: 35.0, name: 'lewlone', text: 'hes been spinning for 9 hours', color: '#c59bff'},
	{at: 36.5, name: 'KirbyUPUP', text: 'its rigged lol', color: '#ff9f6b'},
	{at: 41.0, name: 'BoompjeJunior', text: 'REQ go outside', color: '#6bffd8'},
	{at: 47.2, name: 'kaiib', text: '💀💀💀', color: '#7ad3ff'},
	{at: 52.0, name: 'Emii5287', text: 'rip', color: '#ff7ab6'},
	{at: 56.3, name: '', text: 'lojjkli has joined the experience.', system: true},
	{at: 60.3, name: 'HachiMC', text: 'WHO IS THAT', color: '#ffd166'},
	{at: 62.0, name: 'lojjkli', text: 'hey req :)', color: '#ff5cf0'},
	{at: 63.2, name: 'lojjkli', text: 'marry me?', color: '#ff5cf0'},
	{at: 64.8, name: 'kaiib', text: 'WAIT A WEDDING??', color: '#7ad3ff'},
	{at: 69.0, name: 'lojjkli', text: 'do u promise to stop gambling?', color: '#ff5cf0'},
	{at: 71.4, name: 'GamingSquirrel39', text: 'LETS GOOOO', color: '#9cff8a'},
	{at: 71.8, name: 'Emii5287', text: 'W', color: '#ff7ab6'},
	{at: 72.2, name: 'lewlone', text: 'invite me next time', color: '#c59bff'},
	{at: 75.2, name: 'lojjkli', text: 'REQ.', color: '#ff5cf0'},
	{at: 79.0, name: 'KirbyUPUP', text: 'uh guys', color: '#ff9f6b'},
	{at: 82.3, name: 'HachiMC', text: 'RUNNNNN', color: '#ffd166'},
	{at: 83.0, name: 'BoompjeJunior', text: 'AAAAAAA', color: '#6bffd8'},
	{at: 84.0, name: 'kaiib', text: 'my huge pets 😭', color: '#7ad3ff'},
	{at: 86.5, name: 'lewlone', text: 'who did this', color: '#c59bff'},
];

// kli's bubble-chat lines (shown above kli's head)
export const KLI_BUBBLES = CHAT.filter((c) => c.name === 'lojjkli');
