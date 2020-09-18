from meenkari import models, assets

t = models.Game.objects.all()[1]
print("1", t)

print("2", t.p0)

assets.random_p0(t)

#print("2", t.p0)

assets.display_hands(t)
assets.shuffle_cards(t)
