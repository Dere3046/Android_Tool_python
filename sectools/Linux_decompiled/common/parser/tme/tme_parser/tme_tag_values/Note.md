# TME update notes

The TME format - tags, values, and their relations are defined externally at https://github.qualcomm.com/soc-security-architecture/tme_tag_values. 

Please, follow this link and read the details.

## How to add a new TME protocol version to sectools
1. Create a sub folder matching TME version number.
2. Make sure the TME repo (above) master branch is up-to-date (i.e., TME version you are updating was officially released). See https://github.qualcomm.com/soc-security-architecture/tme_tag_values/blob/master/VERISON.md file for the version.
3. Copy **tme_tags.json**, **tme_relations.json**, **tme_enums.json** files from the above repo (master) branch to a new folder. (No code changes required).
