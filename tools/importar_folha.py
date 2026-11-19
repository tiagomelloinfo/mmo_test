"""Importa uma folha de sprites desenhada fora do jogo (fundo branco) para o formato de assets/.

Recorta cada personagem pelo fundo branco, separa linhas e colunas pela ordem esperada,
alinha os pés e o centro do corpo na mesma posição dos sprites do jogo e grava PNG + JSON.

Uso:
  python3 tools/importar_folha.py protagonista <imagem> <saida_base>
  python3 tools/importar_folha.py npcs <imagem> <saida_base>
"""
import json, sys
from collections import deque
from PIL import Image

# geometria dos sprites humanos do jogo, em unidades lógicas (ver sprHuman)
LW, LH = 33, 42          # tamanho do quadro com contorno
FEET_Y = 37.4            # linha dos pés
CENTER_X = 16.5          # centro do corpo
BODY_H = 30.7            # altura do topo do cabelo aos pés

POSES_PROTAGONISTA = [  # (linha, nomes dos quadros da esquerda para a direita)
    ['f_idle_0', 'f_idle_1'], ['f_walk_0', 'f_walk_1', 'f_walk_2', 'f_walk_3'], ['f_attack_0', 'f_attack_1', 'f_attack_2'],
    ['f_cast_0'], ['f_sit_0'], ['f_dead_0'],
    ['b_idle_0', 'b_idle_1'], ['b_walk_0', 'b_walk_1', 'b_walk_2', 'b_walk_3'], ['b_attack_0', 'b_attack_1', 'b_attack_2'],
    ['b_cast_0'], ['b_sit_0'], ['b_dead_0'],
]
NPCS = ['barkeep', 'innkeep', 'farmer', 'patron2', 'priest', 'merchant', 'master', 'mage', 'guildm', 'soldier', 'guard']
POSES_NPCS = [[f'{n}_f_0', f'{n}_f_1', f'{n}_b_0', f'{n}_b_1'] for n in NPCS]


def tira_fundo(im):
    """Fundo branco ligado às bordas vira transparente (o branco de dentro do desenho fica)."""
    im = im.convert('RGBA'); W, H = im.size; px = im.load()
    claro = lambda p: p[0] > 232 and p[1] > 232 and p[2] > 232
    vis = bytearray(W * H); q = deque()
    for x in range(W):
        for y in (0, H - 1): q.append((x, y))
    for y in range(H):
        for x in (0, W - 1): q.append((x, y))
    while q:
        x, y = q.popleft()
        if x < 0 or y < 0 or x >= W or y >= H or vis[y * W + x]: continue
        vis[y * W + x] = 1
        if not claro(px[x, y]): continue
        px[x, y] = (255, 255, 255, 0)
        q.extend(((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)))
    # halo esbranquiçado colado ao fundo
    for _ in range(2):
        apagar = []
        for y in range(H):
            for x in range(W):
                p = px[x, y]
                if p[3] and min(p[:3]) > 205 and any(0 <= x + dx < W and 0 <= y + dy < H and px[x + dx, y + dy][3] == 0 for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                    apagar.append((x, y))
        for x, y in apagar: px[x, y] = (255, 255, 255, 0)
    return im


def faixas(contagem, minimo=1):
    """Intervalos contínuos onde contagem > 0."""
    out, ini = [], None
    for i, v in enumerate(contagem + [0]):
        if v >= minimo and ini is None: ini = i
        if v < minimo and ini is not None: out.append((ini, i)); ini = None
    return out


def recorta(im, layout):
    W, H = im.size; a = im.getchannel('A').load()
    linhas = faixas([sum(1 for x in range(W) if a[x, y]) for y in range(H)], 1)
    linhas = [l for l in linhas if l[1] - l[0] > 6]
    if len(linhas) != len(layout):
        raise SystemExit(f'esperava {len(layout)} linhas, achei {len(linhas)}: {linhas}')
    quadros = {}
    for (y0, y1), nomes in zip(linhas, layout):
        cols = faixas([sum(1 for y in range(y0, y1) if a[x, y]) for x in range(W)], 1)
        # junta pedaços muito próximos (arma, mão solta) ao vizinho
        juntos = []
        for c in cols:
            if juntos and c[0] - juntos[-1][1] < 4: juntos[-1] = (juntos[-1][0], c[1])
            else: juntos.append(c)
        juntos = [c for c in juntos if c[1] - c[0] > 3]
        if len(juntos) != len(nomes):
            raise SystemExit(f'linha {y0}-{y1}: esperava {len(nomes)} quadros, achei {len(juntos)}: {juntos}')
        for (x0, x1), nome in zip(juntos, nomes):
            ys = [y for y in range(y0, y1) if any(a[x, y] for x in range(x0, x1))]
            quadros[nome] = im.crop((x0, ys[0], x1, ys[-1] + 1))
    return quadros


def centro_pes(fr):
    """Centro horizontal da parte de baixo (pernas), para alinhar mesmo com braço levantado."""
    W, H = fr.size; a = fr.getchannel('A').load(); xs = []
    for y in range(int(H * .7), H):
        xs += [x for x in range(W) if a[x, y]]
    return sum(xs) / len(xs) if xs else W / 2


def monta(quadros, k):
    """Coloca cada recorte num quadro do tamanho dos sprites do jogo, com os pés e o centro no lugar."""
    out = {}
    for nome, fr in quadros.items():
        deitado = '_dead_' in nome
        cw, ch = (round(LH * k), round(LW * k)) if deitado else (round(LW * k), round(LH * k))
        c = Image.new('RGBA', (cw, ch), (0, 0, 0, 0))
        if deitado:
            x = round(cw / 2 - fr.width / 2); y = round(ch - 4.6 * k - fr.height)
        else:
            x = round(CENTER_X * k - centro_pes(fr)); y = round(FEET_Y * k - fr.height)
        c.alpha_composite(fr, (max(0, x), max(0, y)))
        out[nome] = c
    return out


def grava(quadros, k, base, nota):
    pad = 2; cw = max(q.width for q in quadros.values()) + pad * 2; ch = max(q.height for q in quadros.values()) + pad * 2
    cols = 4; nomes = list(quadros); rows = (len(nomes) + cols - 1) // cols
    folha = Image.new('RGBA', (cols * cw, rows * ch), (0, 0, 0, 0)); meta = {}
    for i, n in enumerate(nomes):
        q = quadros[n]; x = (i % cols) * cw + pad; y = (i // cols) * ch + pad
        folha.alpha_composite(q, (x, y)); meta[n] = {'x': x, 'y': y, 'w': q.width, 'h': q.height, 'k': k}
    folha.save(base + '.png')
    nome = base.split('/')[-1] + '.png'
    json.dump({'imagem': nome, 'largura': folha.width, 'altura': folha.height, 'nota': nota, 'quadros': meta}, open(base + '.json', 'w'), ensure_ascii=False, indent=1)
    print(f'{base}: {len(meta)} quadros, k={k:.3f}')


if __name__ == '__main__':
    tipo, img, base = sys.argv[1:4]
    im = tira_fundo(Image.open(img))
    if tipo == 'protagonista':
        q = recorta(im, POSES_PROTAGONISTA)
        k = q['f_idle_0'].height / BODY_H
        grava(monta(q, k), k, base, 'Protagonista desenhado à mão (importado). Mesmas poses do jogo; a arma equipada é desenhada por cima.')
    else:
        q = recorta(im, POSES_NPCS)
        sem_chapeu = [q[f'{n}_f_0'].height for n in ('barkeep', 'patron2', 'master')]
        k = sorted(sem_chapeu)[1] / BODY_H
        grava(monta(q, k), k, base, 'NPCs desenhados à mão (importados): frente 0 e 1, costas 0 e 1.')
