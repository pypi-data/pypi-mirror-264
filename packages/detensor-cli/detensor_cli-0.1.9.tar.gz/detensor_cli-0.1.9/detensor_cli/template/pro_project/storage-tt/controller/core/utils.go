package core

func isAsciiLowercase(ch byte) bool {
	return ch >= 'a' && ch <= 'z'
}

func isAsciiDigit(ch byte) bool {
	return ch >= '0' && ch <= '9'
}

func IsValidRFC1035(name string) bool {
	if len(name) == 0 || len(name) > 63 {
		return false
	}

	for i := 0; i < len(name); i++ {
		ch := name[0]
		if isAsciiLowercase(ch) || isAsciiDigit(ch) || ch == '-' {
			continue
		} else {
			return false
		}
	}

	if !isAsciiLowercase(name[0]) {
		return false
	}

	if name[len(name)-1] == '-' {
		return false
	}

	return true
}
