init 5 python in np_threading:
    import store
    import store.np_globals as np_globals
    import store.np_util as np_util
    import store.mas_threading as mas_threading
    def updateThreadArgs(thread, args):
        """
        Sets new args for the thread
        IN:
            thread - a thread we are changing args for
            args - a list of args
        """
        thread._th_args = args

    def resetThread(thread):
        """
        Resets thread properties so we can start another one
        regardless of if it's ready or not
        IN:
            thread - the thread we reset
        """
        thread._th_result = None
        thread._th_done = True
        thread.ready = True
    
    def _Music_Search():
        return np_util.Music_Search(np_globals.Search_Word)

    Music_Search = mas_threading.MASAsyncWrapper(_Music_Search)
