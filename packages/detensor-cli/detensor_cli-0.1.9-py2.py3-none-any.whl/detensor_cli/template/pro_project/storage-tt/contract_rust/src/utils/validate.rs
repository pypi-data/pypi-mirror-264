/// check name is a valid rfc_1035
pub fn is_valid_rfc_1035(name: &str) -> bool {
    if name.is_empty() || name.len() > 63 {
        return false;
    }

    for ch in name.chars() {
        if ch.is_ascii_lowercase() || ch.is_ascii_digit() || ch == '-' {
            continue;
        } else {
            return false;
        }
    }

    if !name.chars().next().unwrap().is_ascii_alphabetic() {
        return false;
    }

    if name.chars().nth_back(0).unwrap() == '-' {
        return false;
    }

    true
}
