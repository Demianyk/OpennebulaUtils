class _StateWaitingTimedOut(Exception):
    def __init__(self, desired_state, current_state, state_type):
        self.desired_state = desired_state
        self.current_state = current_state
        self.state_type = state_type
        super(_StateWaitingTimedOut, self).__init__()

    def __str__(self):
        return "Time out happened while waiting till VM gets '{}' {}." \
               " The current state is '{}'." \
            .format(self.desired_state, self.state_type, self.current_state)


class LCMStateWaitingTimedOut(_StateWaitingTimedOut):
    def __init__(self, desired_state, current_state):
        super(LCMStateWaitingTimedOut, self).__init__(desired_state,
                                                      current_state,
                                                      'lcm_state')


class StateWaitingTimedOut(_StateWaitingTimedOut):
    def __init__(self, desired_state, current_state):
        super(StateWaitingTimedOut, self).__init__(desired_state,
                                                   current_state,
                                                   'state')
