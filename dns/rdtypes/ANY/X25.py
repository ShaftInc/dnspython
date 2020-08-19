# Copyright (C) Dnspython Contributors, see LICENSE for text of ISC license

# Copyright (C) 2003-2007, 2009-2011 Nominum, Inc.
#
# Permission to use, copy, modify, and distribute this software and its
# documentation for any purpose with or without fee is hereby granted,
# provided that the above copyright notice and this permission notice
# appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND NOMINUM DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL NOMINUM BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT
# OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

import struct

import dns.exception
import dns.immutable
import dns.rdata
import dns.tokenizer


@dns.immutable.immutable
class X25(dns.rdata.Rdata):

    """X25 record"""

    # see RFC 1183

    __slots__ = ['address']

    def __init__(self, rdclass, rdtype, address):
        super().__init__(rdclass, rdtype)
        if isinstance(address, str):
            self.address = self.as_value(address.encode())
        else:
            self.address = self.as_value(address)

    def to_text(self, origin=None, relativize=True, **kw):
        return '"%s"' % dns.rdata._escapify(self.address)

    @classmethod
    def from_text(cls, rdclass, rdtype, tok, origin=None, relativize=True,
                  relativize_to=None):
        address = tok.get_string()
        return cls(rdclass, rdtype, address)

    def _to_wire(self, file, compress=None, origin=None, canonicalize=False):
        l = len(self.address)
        assert l < 256
        file.write(struct.pack('!B', l))
        file.write(self.address)

    @classmethod
    def from_wire_parser(cls, rdclass, rdtype, parser, origin=None):
        address = parser.get_counted_bytes()
        return cls(rdclass, rdtype, address)
