/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, onWillStart, useState } from "@odoo/owl";
import { standardFieldProps } from "@web/views/fields/standard_field_props";

class LeadQualityDropdown extends Component {
    setup() {
        this.state = useState({ value: this.props.value || "" });

        this.colorMap = {
            "hot": "red",
            "warm": "orange",
            "cold": "blue",
            "bad": "gray",
            "not_responding": "black",
            "crash": "darkgray"
        };
    }

    onChange(ev) {
        this.state.value = ev.target.value;
        this.props.update(ev.target.value);
    }
}

LeadQualityDropdown.template = "custom_leads.LeadQualityDropdown";
LeadQualityDropdown.props = standardFieldProps;
LeadQualityDropdown.supportedTypes = ["selection"];

// Register the custom field
registry.category("fields").add("lead_quality_dropdown", LeadQualityDropdown);
