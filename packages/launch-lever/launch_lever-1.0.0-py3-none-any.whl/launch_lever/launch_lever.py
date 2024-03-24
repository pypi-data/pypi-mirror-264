class LaunchLever:
    def __init__(self, toggle_data):
        self.toggles = toggle_data

    def get_toggle(self, toggle_name):
        toggle = None
        for t in self.toggles:
            if t["name"] == toggle_name:
                toggle = t
        return toggle

    def is_on(self, toggle_name):
        toggle = self.get_toggle(toggle_name)
        if not toggle:
            return False
        return toggle["status"] == "on"
