from reader import Entry, Reader, CachedReader

entries = Entry.symbols('list_final', ' :: ')
entries = entries[0:3]

#Reader('access_key', entries).pull()

c = CachedReader('access_key', entries, 'cached')
#c.fill_cache()
print([e.name for e in c.cache_entries()])
c.pull()

#for entry in entries:
#    print(entry.name, entry.data)

