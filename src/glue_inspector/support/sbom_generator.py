import logging
import sys
from typing import TYPE_CHECKING

from cyclonedx.builder.this import this_component as cdx_lib_component
from cyclonedx.exception import MissingOptionalDependencyException
from cyclonedx.model import ExternalReference, ExternalReferenceType, XsUri
from cyclonedx.model.bom import Bom
from cyclonedx.model.component import Component, ComponentType
from cyclonedx.output.json import JsonV1Dot5
from cyclonedx.schema import SchemaVersion
from cyclonedx.validation.json import JsonStrictValidator
from packageurl import PackageURL

from glue_inspector.support.requirements import Requirements

if TYPE_CHECKING:
    from cyclonedx.output.json import Json as JsonOutputter


class SBomGenerator:
    def __init__(self, name: str, requirements: Requirements):
        self.name: str = name
        self.requirements: Requirements = requirements
        self._index_url = "https://pypi.org/simple"
        pass

    def generate(self):
        """_summary_"""
        # lc_factory = LicenseFactory()

        # region build the BOM

        self.bom = Bom()
        self.bom.metadata.tools.components.add(cdx_lib_component())
        self.bom.metadata.tools.components.add(
            Component(
                name="Glue Inspector",
                type=ComponentType.APPLICATION,
            )
        )

        self.bom.metadata.component = root_component = Component(
            name=self.name,
            type=ComponentType.APPLICATION,
            # licenses=[lc_factory.make_from_string('MIT')],
            bom_ref=self.name,
        )

        for requirement in self.requirements.data.values():
            component = Component(
                name=requirement.name,
                version=requirement.version,
                type=ComponentType.LIBRARY,
                # licenses=[lc_factory.make_from_string('MIT')],
                bom_ref=f"{requirement.name}@{requirement.version}",
                purl=PackageURL(name=requirement.name, version=requirement.version, type="pypi"),
                external_references=[
                    ExternalReference(
                        comment="implicit dist url",
                        type=ExternalReferenceType.DISTRIBUTION,
                        url=XsUri(f"{self._index_url}/{requirement.name}/"),
                    )
                ],
            )
            self.bom.components.add(component)
            self.bom.register_dependency(root_component, [component])

        return self.bom

    def get_json(self, validate=False):
        """_summary_

        Returns:
            str: _description_
        """
        my_json_outputter: "JsonOutputter" = JsonV1Dot5(self.bom)
        serialized_json = my_json_outputter.output_as_string(indent=2)

        if validate:
            self.validate_json(serialized_json)

        return serialized_json

    def validate_json(self, json_data):
        """Validate the JSON data against the CycloneDX JSON schema."""

        my_json_validator = JsonStrictValidator(SchemaVersion.V1_6)
        try:
            validation_errors = my_json_validator.validate_str(json_data)
            if validation_errors:
                logging.error("JSON invalid", "ValidationError:", repr(validation_errors))
                sys.exit(2)
            logging.debug("JSON valid")

        except MissingOptionalDependencyException as error:
            logging.error("JSON-validation was skipped due to", error)
            return False

        return True
