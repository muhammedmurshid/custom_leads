/** @odoo-module **/
import { ProgressBarField } from "@web/views/fields/progress_bar/progress_bar_field";
import { patch } from "@web/core/utils/patch";

patch(ProgressBarField.prototype, {
    setup() {
        super.setup(...arguments);
        // Additional setup if needed
    },

    get progressBarColorClass() {
        // Map lead_quality values to specific colors
        const leadQualityColors = {
            new: "o_progress_info",
            waiting_for_admission: "o_progress_primary",
            admission: "o_progress_success",
            hot: "o_progress_danger",
            warm: "o_progress_warning",
            cold: "o_progress_light",
            bad_lead: "o_progress_dark",
            not_responding: "o_progress_secondary",
            crash_lead: "o_progress_muted",
            nil: "o_progress_secondary",
        };

        // Retrieve the value of the lead_quality field
        const leadQuality = this.record.data.lead_quality;

        // Return the corresponding CSS class for the lead_quality value
        return leadQualityColors[leadQuality] || "bg-primary";
    },
});
