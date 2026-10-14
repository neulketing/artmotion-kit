// ArtMotion Kit demo: three art styles with Korean on-screen text (about 7 s).
// Copy into a project copy of scripts/engine/ after l10n/apply.sh, then:
//   uv run --with playwright python <engine>/render.py --film ko --fps 30 --out demo_ko.mp4
// Hangul comes from the PuHui-* families (Noto Sans KR via the l10n unicode-range faces).
const band = c => { c.save(); const g = c.createLinearGradient(0, 820, 0, 1080); g.addColorStop(0, 'rgba(16,14,12,0)'); g.addColorStop(0.35, 'rgba(16,14,12,.62)'); g.addColorStop(1, 'rgba(16,14,12,.78)'); c.fillStyle = g; c.fillRect(0, 820, 1920, 260); c.restore(); };
const tag = (year, name, sub) => ({ mode: 'tag', year, name, sub, box: band, align: 'center', x: 960, y: 905, size: 50,
  font: 'PuHui-Bold', color: '#f5d03b', nameFont: '84px "PuHui-Black"', nameColor: '#fff8e6', ny: 995, subFont: '38px "PuHui-Medium"', subColor: '#e8dcc4', sy: 1050 });
window.ERAS = [
  { id: '29_seurat', eighths: 10, counter: tag(1884, '쇠라, 점으로 빛을 쌓다', '신인상주의 · 그랑드자트 섬의 일요일 오후') },
  { id: '09_postimp', eighths: 10, transition: { type: 'swirl', dur: 0.4, cx: 560, cy: 340 }, counter: tag(1889, '고흐, 방 안까지 붓결로 채우다', '후기 인상주의 · 아를의 침실과 해바라기') },
  { id: '28_monet', eighths: 10, transition: { type: 'ripple', dur: 0.45, cx: 1000, cy: 600 }, counter: tag(1899, '모네, 물 위에 시간을 그리다', '인상주의 · 수련과 일본식 다리') },
];
