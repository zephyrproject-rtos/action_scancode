#!/usr/bin/env python3

# Copyright (c) 2018 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

import argparse
import sys
import json
import yaml

def analyze_file(config_file, scancode_file, scanned_files_dir):

    with open(config_file, 'r') as f:
        config = yaml.safe_load(f.read())

    report = ""

    exclude = config.get("exclude")
    if exclude:
        never_check_ext =  exclude.get("extensions", [])
        never_check_langs = exclude.get("langs", [])
    else:
        never_check_ext = []
        never_check_langs = []

    copyrights = config.get("copyright", {})
    check_copytight = copyrights.get("check", False)
    lic_config = config.get("license")
    lic_main = lic_config.get("main")
    lic_cat = lic_config.get("category")
    report_missing_license = lic_config.get("report_missing", False)
    more_cat = []
    more_cat.append(lic_cat)
    more_lic = lic_config.get('additional', [])
    more_lic.append(lic_main)

    # Scancode may report 'unknown-license-reference' if there are lines
    # containing the word 'license' in the source files, so ignore these for
    # now.
    more_cat.append('Unstated License')
    more_lic.append('unknown-license-reference')

    if check_copytight:
        print("Will check for missing copyrights...")

    check_langs = []
    with open(scancode_file, 'r') as json_fp:
        scancode_results = json.load(json_fp)
        for file in scancode_results['files']:
            if file['type'] == 'directory':
                continue

            orig_path = str(file['path']).replace(scanned_files_dir, '')
            licenses = file['licenses']
            file_type = file.get("file_type")
            kconfig = "Kconfig" in orig_path and file_type in ['ASCII text']
            check = False

            if file.get("extension")[1:] in never_check_ext:
                check = False
            elif file.get("programming_language") in never_check_langs:
                check = False
            elif kconfig:
                check = True
            elif file.get("programming_language") in check_langs:
                check = True
            elif file.get("is_script"):
                check = True
            elif file.get("is_source"):
                check = True

            if check:
                if not licenses and not report_missing_license:
                    report += ("* {} missing license.\n".format(orig_path))
                else:
                    for lic in licenses:
                        if lic['key'] not in more_lic:
                            report += ("* {} has invalid license: {}\n".format(
                                orig_path, lic['key']))
                        if lic['category'] not in more_cat:
                            report += ("* {} has invalid license type: {}\n".format(
                                orig_path, lic['category']))
                        if lic['key'] == 'unknown-spdx':
                            report += ("* {} has unknown SPDX: {}\n".format(
                                orig_path, lic['key']))

                if check_copytight and not file['copyrights'] and \
                        file.get("programming_language") != 'CMake':
                    report += ("* {} missing copyright.\n".format(orig_path))


    return(report)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Analyze licenses...")
    parser.add_argument('-s', '--scancode-output',
                        help='''JSON output from scancode-toolkit''')
    parser.add_argument('-f', '--scanned-files',
                        help="Directory with scanned files")
    parser.add_argument('-c', '--config-file',
                        help="Configuration file")
    parser.add_argument('-o', '--output-file',
                        help="Output report file")
    return parser.parse_args()

if __name__ == "__main__":

    args = parse_args()


    if args.scancode_output and args.scanned_files and args.config_file:
        report = analyze_file(args.config_file, args.scancode_output, args.scanned_files)
        if report:
            with open(args.output_file, "w") as fp:
                fp.write(report)
    else:
        sys.exit("Provide files to analyze")
