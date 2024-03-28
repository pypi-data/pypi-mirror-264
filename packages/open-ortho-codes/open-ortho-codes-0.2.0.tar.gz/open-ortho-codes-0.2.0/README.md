[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/open-ortho/codes">
    <img src="https://raw.githubusercontent.com/open-ortho/dicom4ortho/master/images/open-ortho.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">open-ortho codes</h3>

  <p align="center">
    A collection of codes and terms from various terminologies, specifically tailored for software development within the orthodontic domain.
    <br />
    <a href="https://open-ortho.github.io/codes/"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/open-ortho/codes">View Demo</a>
    ·
    <a href="https://github.com/open-ortho/codes/issues">Report Bug</a>
    ·
    <a href="https://github.com/open-ortho/codes/issues">Request Feature</a>
  </p>
</p>

## About The Project

This project serves as a centralized repository for orthodontic software developers, offering a curated collection of essential codes required for implementing healthcare standards like DICOM or HL7. Navigating through various terminologies to find the right codes can be challenging. Our project aims to simplify this process by providing a go-to source for these codes, readily available in JSON and CSV formats. Users can access these directly through GitHub releases or utilize them as a Python package on PyPI.

## Using The Codes

### Python

If you want to use the codes directly in your Python project:

    pip install open-ortho-codes

Then

    from ortho_codes import hl7 as codes_hl7

    print(f"{codes_hl7.orthodontic.system}")
    print(codes_hl7.orthodontic.code)
    print(codes_hl7.orthodontic.display)

Convert codes to JSON

    from ortho_codes import hl7 as codes_hl7

    print(f"{codes_hl7.orthodontic.to_json()}")

### JSON

Just point your code to any of the following:


## Releases

- Each new release must be git tagged with v*.*.*. This triggers the Github actions to publish to PyPi and release in GitHub releases.
- 

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/open-ortho/codes.svg?style=for-the-badge
[contributors-url]: https://github.com/open-ortho/codes/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/open-ortho/codes.svg?style=for-the-badge
[forks-url]: https://github.com/open-ortho/codes/network/members
[stars-shield]: https://img.shields.io/github/stars/open-ortho/codes.svg?style=for-the-badge
[stars-url]: https://github.com/open-ortho/codes/stargazers
[issues-shield]: https://img.shields.io/github/issues/open-ortho/codes.svg?style=for-the-badge
[issues-url]: https://github.com/open-ortho/codes/issues
[license-shield]: https://img.shields.io/github/license/open-ortho/codes.svg?style=for-the-badge
[license-url]: https://github.com/open-ortho/codes/blob/master/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/open-ortho
[product-screenshot]: images/screenshot.png
[example-csv-url]: resources/example/input_from.csv