class StatusResult:
    def __init__(self, untracked, staged, modified):
        self.untracked = untracked
        self.staged = staged
        self.modified = modified