
from dataclasses import dataclass
from profile.schema import FuseBlowing, FuseRow
FuseArgument = dataclass(<NODE:12>)
security_profile_data: FuseBlowing | None = None
multi_row_full_region_fuses: dict[(str, list[FuseRow])] = { }
multi_row_partial_region_fuses: dict[(str, list[FuseRow])] = { }
fuse_groups: dict[(str, list[FuseArgument])] = { }
recommended_fuses_qti_values: dict[(str, str)] = { }
recommended_fuses_oem_values: list[str] = []
oem_choice_fuses: list[str] = []
