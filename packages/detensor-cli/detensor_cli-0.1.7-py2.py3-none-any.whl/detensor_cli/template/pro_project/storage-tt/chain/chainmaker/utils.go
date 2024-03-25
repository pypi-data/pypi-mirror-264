package chainmaker

import "encoding/binary"

func EncodeUint64(n uint64) []byte {
	ret := make([]byte, 8)
	binary.BigEndian.PutUint64(ret, n)
	return ret
}

func EncodeBool(b bool) []byte {
	ret := make([]byte, 1)
	if b {
		ret[0] = 1
	} else {
		ret[0] = 0
	}
	return ret
}
