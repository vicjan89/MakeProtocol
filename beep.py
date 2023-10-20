import winsound
# Воспроизвести звук выхода из Windows.
sounds = ('SystemExclamation', 'SystemAsterisk', 'SystemExit', 'SystemHand', 'SystemQuestion')
for i in range(2):
    winsound.PlaySound(sounds[3], winsound.SND_ALIAS)

# Вероятно, воспроизводится звук Windows по умолчанию, если он зарегистрирован (потому что
# "*" вероятно, это не зарегистрированное название какого-либо звука).
# winsound.PlaySound("*", winsound.SND_ALIAS)