import struct, zlib, sys, os, json

class OLE:
    def __init__(self, path):
        d = open(path, 'rb').read()
        self.d = d
        assert d[:8] == b'\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1'
        self.ss = 1 << struct.unpack_from('<H', d, 30)[0]
        self.mss = 1 << struct.unpack_from('<H', d, 32)[0]
        nfat = struct.unpack_from('<I', d, 44)[0]
        dirstart = struct.unpack_from('<I', d, 48)[0]
        self.cutoff = struct.unpack_from('<I', d, 56)[0]
        minifatstart = struct.unpack_from('<I', d, 60)[0]
        difstart = struct.unpack_from('<I', d, 68)[0]
        ndif = struct.unpack_from('<I', d, 72)[0]
        difat = list(struct.unpack_from('<109I', d, 76))
        s = difstart
        for _ in range(ndif):
            sec = self.sec(s)
            vals = struct.unpack('<%dI' % (self.ss // 4), sec)
            difat += vals[:-1]
            s = vals[-1]
        difat = [x for x in difat[:nfat]]
        self.fat = []
        for s in difat:
            self.fat += struct.unpack('<%dI' % (self.ss // 4), self.sec(s))
        dirdata = self.chain(dirstart)
        self.entries = []
        for i in range(len(dirdata) // 128):
            e = dirdata[i*128:(i+1)*128]
            nl = struct.unpack_from('<H', e, 64)[0]
            name = e[:max(nl-2, 0)].decode('utf-16le')
            typ = e[66]
            left, right, child = struct.unpack_from('<III', e, 68)
            start, size = struct.unpack_from('<II', e, 116)
            self.entries.append(dict(name=name, typ=typ, left=left, right=right, child=child, start=start, size=size))
        root = self.entries[0]
        self.ministream = self.chain(root['start'])[:root['size']] if root['start'] < 0xFFFFFFF0 else b''
        self.minifat = []
        if minifatstart < 0xFFFFFFF0:
            mf = self.chain(minifatstart)
            self.minifat = list(struct.unpack('<%dI' % (len(mf)//4), mf))
        self.paths = {}
        self.walk(root['child'], '')

    def sec(self, i):
        o = 512 + i * self.ss
        return self.d[o:o+self.ss]

    def chain(self, s):
        out = []
        seen = 0
        while s < 0xFFFFFFF0 and seen < 1000000:
            out.append(self.sec(s)); s = self.fat[s]; seen += 1
        return b''.join(out)

    def minichain(self, s):
        out = []
        while s < 0xFFFFFFF0:
            o = s * self.mss
            out.append(self.ministream[o:o+self.mss]); s = self.minifat[s]
        return b''.join(out)

    def walk(self, i, prefix):
        if i == 0xFFFFFFFF or i >= len(self.entries): return
        e = self.entries[i]
        p = prefix + e['name']
        self.paths[p] = e
        self.walk(e['left'], prefix); self.walk(e['right'], prefix)
        if e['typ'] == 1: self.walk(e['child'], p + '/')

    def read(self, p):
        e = self.paths[p]
        if e['size'] < self.cutoff:
            return self.minichain(e['start'])[:e['size']]
        return self.chain(e['start'])[:e['size']]

SINGLE = {0, 10, 13, 24, 25, 26, 27, 28, 29, 30, 31}

def para_text(b):
    out = []
    i = 0
    n = len(b) // 2
    while i < n:
        c = struct.unpack_from('<H', b, i*2)[0]
        if c < 32:
            if c in SINGLE:
                if c == 10: out.append('\n')
                elif c == 13: pass
                elif c == 24: out.append('-')
                elif c == 30 or c == 31: out.append(' ')
                i += 1
            else:
                if c == 9: out.append('\t')
                i += 8
        else:
            out.append(chr(c)); i += 1
    return ''.join(out)

def records(data):
    i = 0
    while i + 4 <= len(data):
        h = struct.unpack_from('<I', data, i)[0]; i += 4
        tag = h & 0x3FF; lvl = (h >> 10) & 0x3FF; sz = h >> 20
        if sz == 0xFFF:
            sz = struct.unpack_from('<I', data, i)[0]; i += 4
        yield tag, lvl, data[i:i+sz]
        i += sz

def extract(path):
    o = OLE(path)
    fh = o.read('FileHeader')
    flags = struct.unpack_from('<I', fh, 36)[0]
    compressed = flags & 1
    dist = flags & 4
    secs = sorted([p for p in o.paths if p.startswith('BodyText/Section')], key=lambda x: int(x.split('Section')[1]))
    out = []
    for s in secs:
        data = o.read(s)
        if compressed: data = zlib.decompress(data, -15)
        # track tables: TABLE tag 0x10+61=77, LIST_HEADER 0x10+56=72, PARA_HEADER 66, PARA_TEXT 67, CTRL_HEADER 71
        for tag, lvl, body in records(data):
            if tag == 71:
                cid = body[:4][::-1].decode('latin1', 'replace')
                if cid == 'tbl ': out.append(('\x01TABLE', lvl))
            elif tag == 72:
                out.append(('\x01CELL', lvl))
            elif tag == 66:
                out.append(('\x01PARA', lvl))
            elif tag == 67:
                out.append((para_text(body), lvl))
    return o, flags, out

if __name__ == '__main__':
    o, flags, out = extract(sys.argv[1])
    print('flags', flags, file=sys.stderr)
    for t, l in out:
        if t.startswith('\x01'):
            if t != '\x01PARA': print('  ' * l + '[' + t[1:] + ']')
        else:
            print('  ' * l + t)
