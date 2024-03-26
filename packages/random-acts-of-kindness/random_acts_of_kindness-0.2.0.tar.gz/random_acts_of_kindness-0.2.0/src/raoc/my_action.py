"""."""

import random


ACTS_OF_KINDNESS = {
    "Pick Up Trash: Go for a walk around your neighborhood or a local park and pick up litter together. It's a simple act that can have a big impact on the environment.",
    "Help with Chores: Offer to help a family member or neighbor with chores like gardening, cleaning, or grocery shopping without expecting anything in return.",
    "Visit Elderly Neighbors: Take some time to visit elderly neighbors and spend time chatting with them. It can brighten their day and make them feel less lonely.",
}


class MyAction:
    """."""
    def __init__(self) -> None:
        """."""
        self.already_suggested: set[str] = set()

    def get_random_act_and_explanation(self) -> tuple[str, str]:
        """."""
        if len(ACTS_OF_KINDNESS) == len(self.already_suggested):
            self.already_suggested = set()

        remaining_set = list(ACTS_OF_KINDNESS - self.already_suggested)
        act_and_explanation: str = random.choice(remaining_set)
        self.already_suggested.add(act_and_explanation)
        split = act_and_explanation.split(':')
        act = split[0]
        explanation = ''.join(split[1:])
        return act, explanation
