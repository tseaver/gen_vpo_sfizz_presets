"""Generate LV2 presets for sfizz from the Virtual Playing Orchestra"""

import argparse
import pathlib
import shutil

HOME = pathlib.Path("~/").expanduser().resolve()


def build_parser():
    parser = argparse.ArgumentParser(prog=__package__, description=__doc__)
    parser.add_argument(
        "vpo_sfz_files",
        metavar="VPO_SFZ",
        nargs="+",
        help="""\
VPO SFZ files for which to create presets.  If passed as a directory, glob it
recursively to find SFZ files, confirming each unless '--no-confirm-globbed-sfzs'
is passed.
"""
    )
    parser.add_argument(
        "--sfizz-lv2-directory",
        action="store",
        default="/usr/lib/lv2/sfizz.lv2",
        help="Directory to which the sfizz LV2 plugin is installed",
    )
    parser.add_argument(
        "--lv2-preset-directory",
        action="store",
        default=f"{HOME}/.lv2",
        help="Directory into which to place the generated LV2 presets",
    )
    parser.add_argument(
        "--overwrite-lv2-preset",
        action="store_true",
        help="Overwrite existing LV2 presets?",
    )
    parser.add_argument(
        "--no-confirm-globbed-sfzs",
        action="store_true",
        help="Overwrite existing LV2 presets?",
    )


    return parser


def get_preset_ttl(preset_name, sfz_filename):
    return f"""\
@prefix atom: <http://lv2plug.in/ns/ext/atom#> .
@prefix lv2: <http://lv2plug.in/ns/lv2core#> .
@prefix pset: <http://lv2plug.in/ns/ext/presets#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix state: <http://lv2plug.in/ns/ext/state#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<>
	a pset:Preset ;
	lv2:appliesTo <http://sfztools.github.io/sfizz> ;
	rdfs:label "{preset_name}" ;
	lv2:port [
		lv2:symbol "freewheeling" ;
		pset:value 0.0
	] , [
		lv2:symbol "freewheeling_oscillator_quality" ;
		pset:value 3.0
	] , [
		lv2:symbol "freewheeling_sample_quality" ;
		pset:value 10.0
	] , [
		lv2:symbol "num_voices" ;
		pset:value 64.0
	] , [
		lv2:symbol "oscillator_quality" ;
		pset:value 1.0
	] , [
		lv2:symbol "oversampling" ;
		pset:value 1.0
	] , [
		lv2:symbol "preload_size" ;
		pset:value 8192.0
	] , [
		lv2:symbol "sample_quality" ;
		pset:value 2.0
	] , [
		lv2:symbol "scala_root_key" ;
		pset:value 60.0
	] , [
		lv2:symbol "stretched_tuning" ;
		pset:value 0.0
	] , [
		lv2:symbol "sustain_cancels_release" ;
		pset:value 0.0
	] , [
		lv2:symbol "tuning_frequency" ;
		pset:value 440.0
	] , [
		lv2:symbol "volume" ;
		pset:value 0.0
	] ;
	state:state [
		<http://sfztools.github.io/sfizz:sfzfile> <{sfz_filename.name}> ;
		<http://sfztools.github.io/sfizz:tuningfile> <DefaultScale.scl> ;
		<http://sfztools.github.io/sfizz#cc001> "0.5"^^xsd:float ;
		<http://sfztools.github.io/sfizz#cc007> "1.0"^^xsd:float ;
		<http://sfztools.github.io/sfizz#cc010> "1.0"^^xsd:float ;
		<http://sfztools.github.io/sfizz#cc011> "1.0"^^xsd:float
	] .

"""


def get_manifest_ttl(preset_name):
    return f"""\
@prefix atom: <http://lv2plug.in/ns/ext/atom#> .
@prefix lv2: <http://lv2plug.in/ns/lv2core#> .
@prefix pset: <http://lv2plug.in/ns/ext/presets#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix state: <http://lv2plug.in/ns/ext/state#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<{preset_name}.ttl>
	lv2:appliesTo <http://sfztools.github.io/sfizz> ;
	a pset:Preset ;
	rdfs:seeAlso <{preset_name}.ttl> .
"""

class NotOverwritingExistingLV2(Exception):

    def __init__(self, preset_lv2):
        self.preset_lv2 = preset_lv2
        super().__init__(
            f"Not overwriting existing LV2 preset: {preset_lv2}"
        )

class UserQuit():
    pass


def make_lv2_preset(sfz_filename, args):
    sfizz_lv2_directory = pathlib.Path(args.sfizz_lv2_directory)
    sfizz_default_scale_scl = sfizz_lv2_directory / "Contents/Resources/DefaultScale.scl"
    lv2_preset_directory = pathlib.Path(args.lv2_preset_directory)
    section = sfz_filename.parent.name
    preset_name = f"VPO_{section}_{sfz_filename.stem}"
    print(f"- Creating LV2 preset: {preset_name}")

    preset_lv2 = lv2_preset_directory / f"sfizz_{preset_name}.lv2"

    if preset_lv2.exists():

        if not args.overwrite_lv2_preset:
            raise NotOverwritingExistingLV2(preset_lv2)

        shutil.rmtree(preset_lv2)

    preset_lv2.mkdir(parents=True)

    preset_default_scale_scl = preset_lv2 / "DefaultScale.scl"
    preset_default_scale_scl.symlink_to(sfizz_default_scale_scl)

    preset_sfz_file = preset_lv2 / sfz_filename.name
    preset_sfz_file.symlink_to(sfz_filename)

    manifest_ttl = preset_lv2 / "manifest.ttl"
    manifest_ttl.write_text(get_manifest_ttl(preset_name))

    preset_ttl = preset_lv2 / f"{preset_name}.ttl"
    preset_ttl.write_text(get_preset_ttl(preset_name, sfz_filename))

def glob_sfzs(sfz_filename):
    assert sfz_filename.is_dir()
    for globbed in sfz_filename.rglob("*.sfz"):
        confirm = input(f"Use this SFZ: {globbed.name}? [yNq] ")

        if confirm == "y":
            yield globbed

        elif confirm == "q":
            yield UserQuit()

def main():
    parser = build_parser()
    args = parser.parse_args()

    for sfz in args.vpo_sfz_files:
        sfz_filename = pathlib.Path(sfz).resolve()

        if sfz_filename.is_file():
            try:
                make_lv2_preset(sfz_filename, args)
            except NotOverwritingExistingLV2 as e:
                print(str(e))
                continue

        elif sfz_filename.is_dir():

            for globbed in glob_sfzs(sfz_filename):
                if isinstance(globbed, UserQuit):
                    return
                try:
                    make_lv2_preset(globbed, args)
                except NotOverwritingExistingLV2 as e:
                    print(str(e))


if __name__ == "__main__":
    main()
