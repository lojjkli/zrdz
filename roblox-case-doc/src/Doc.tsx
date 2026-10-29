import {AbsoluteFill, Sequence, interpolate, useCurrentFrame} from 'remotion';

type Scene = {kicker?: string; title: string; body?: string; source?: string; secs: number; accent?: string};

const scenes: Scene[] = [
  {kicker: 'A short documentary', title: 'The Roblox Case in Iraq', body: 'What credible news outlets have reported, and what is still unconfirmed.', secs: 5},
  {kicker: '20 October 2025', title: 'Iraq bans Roblox', body: "The Ministry of Communications blocked the platform, citing risks to children such as exploitation and blackmail.", source: 'Al Arabiya · Asharq Al-Awsat', secs: 6},
  {kicker: 'About a week later', title: 'A teenager is arrested', body: "Iraq's Interior Ministry announced the arrest of a teenage boy, reported to be 14 years old.", source: "Al-Hadeel citing Maj. Gen. Mustafa al-Yasiri · Gulf News", secs: 6},
  {kicker: 'The allegations', title: 'Online "challenges"', body: 'Police allege he ran around 16 online networks that used Roblox to pressure children and teens into escalating "challenges", self-harm and suicide.', source: 'Gulf News, 30 Oct 2025', secs: 7},
  {kicker: 'The reported toll', title: '30 young lives', body: 'Officials linked the case to the deaths of about 30 young people in several countries.', source: 'Gulf News · GDN Online, 2 Nov 2025', secs: 6},
  {kicker: 'What is not confirmed', title: 'Allegations, not a verdict', body: 'The suspect is a minor and has not been publicly named. Online claims tying the case to the alias "REQ" or to one specific game do not appear in the news reports we found.', secs: 8, accent: '#f5b942'},
  {kicker: 'Warning signs', title: 'Know the pattern', body: 'Secret "challenges". Pressure to hurt yourself. Threats if you stop. If you see this online: stop, block, report, and tell an adult you trust.', secs: 7},
  {kicker: "You're not alone", title: 'Help is available', body: 'Switzerland: call 143 (Die Dargebotene Hand) or 147 (Pro Juventute, for young people). Anywhere else: findahelpline.com', secs: 7, accent: '#5fd3a1'},
];

const FPS = 30;
export const TOTAL = scenes.reduce((s, x) => s + x.secs * FPS, 0);

const Card = ({s}: {s: Scene}) => {
  const f = useCurrentFrame();
  const dur = s.secs * FPS;
  const op = interpolate(f, [0, 15, dur - 15, dur], [0, 1, 1, 0], {extrapolateRight: 'clamp'});
  const y = interpolate(f, [0, 20], [30, 0], {extrapolateRight: 'clamp'});
  const accent = s.accent ?? '#e2483d';
  return (
    <AbsoluteFill style={{opacity: op, padding: '0 180px', justifyContent: 'center', transform: `translateY(${y}px)`}}>
      {s.kicker && <div style={{color: accent, fontSize: 34, letterSpacing: 6, textTransform: 'uppercase', marginBottom: 24}}>{s.kicker}</div>}
      <div style={{color: '#fff', fontSize: 100, fontWeight: 800, lineHeight: 1.05}}>{s.title}</div>
      <div style={{width: interpolate(f, [10, 40], [0, 220], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}), height: 6, background: accent, margin: '36px 0'}} />
      {s.body && <div style={{color: '#d6d9e0', fontSize: 46, lineHeight: 1.4, maxWidth: 1450}}>{s.body}</div>}
      {s.source && <div style={{position: 'absolute', bottom: 70, left: 180, color: '#8a90a0', fontSize: 28}}>Source: {s.source}</div>}
    </AbsoluteFill>
  );
};

export const Doc = () => {
  const f = useCurrentFrame();
  let start = 0;
  return (
    <AbsoluteFill style={{fontFamily: 'Helvetica, Arial, sans-serif', background: `radial-gradient(circle at ${30 + (f / TOTAL) * 40}% 40%, #1d2233 0%, #0a0c12 70%)`}}>
      {scenes.map((s, i) => {
        const from = start;
        start += s.secs * FPS;
        return (
          <Sequence key={i} from={from} durationInFrames={s.secs * FPS}>
            <Card s={s} />
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};
