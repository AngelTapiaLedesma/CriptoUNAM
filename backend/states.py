from schemas import ReportStatus


ALLOWED_TRANSITIONS = {
    ReportStatus.SUBMITTED: {
        ReportStatus.NEEDS_INFORMATION,
        ReportStatus.VALIDATED,
        ReportStatus.REJECTED,
    },

    ReportStatus.NEEDS_INFORMATION: {
        ReportStatus.SUBMITTED,
        ReportStatus.VALIDATED,
        ReportStatus.REJECTED,
    },

    ReportStatus.VALIDATED: {
        ReportStatus.PAID,
    },

    ReportStatus.PAID: {
        ReportStatus.REMEDIATED,
    },

    ReportStatus.REMEDIATED: {
        ReportStatus.VERIFIED,
    },

    ReportStatus.REJECTED: set(),
    ReportStatus.VERIFIED: set(),
}


def transition_is_allowed(
    current_status: ReportStatus,
    new_status: ReportStatus,
) -> bool:

    allowed = ALLOWED_TRANSITIONS.get(
        current_status,
        set(),
    )

    return new_status in allowed