class CidrMaskConvert:
    @staticmethod
    def cidr_to_mask(val):
        try:
            val = int(val)
            if val < 1 or val > 32:
                raise ValueError
        except ValueError:
            return "Invalid"
        mask = (0xFFFFFFFF << (32 - val)) & 0xFFFFFFFF
        return (
            str((mask >> 24) & 0xFF)
            + "."
            + str((mask >> 16) & 0xFF)
            + "."
            + str((mask >> 8) & 0xFF)
            + "."
            + str(mask & 0xFF)
        )

    @staticmethod
    def mask_to_cidr(val):
        try:
            mask = sum([bin(int(x)).count("1") for x in val.split(".")])
            return str(mask)
        except ValueError:
            return "Invalid"


class IpValidate:
    @staticmethod
    def ipv4_validation(val):
        parts = val.split(".")
        if len(parts) != 4:
            return False
        for part in parts:
            if not part.isdigit() or not 0 <= int(part) <= 255:
                return False
        return True
