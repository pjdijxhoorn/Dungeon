from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_shop_inventory():
    """ Test the endpoint for retrieving shop inventory. """
    response = client.get("/shop")
    assert response.status_code == 200
    assert response.json() == [{'gear_class': 'common',
                                'gear_id': 1,
                                'gear_name': 'Baseball Cap',
                                'gear_price': 20,
                                'gear_slot': 'Head',
                                'gear_stat': 10,
                                'gear_stat_type': 'defence'},
                               {'gear_class': 'uncommon',
                                'gear_id': 2,
                                'gear_name': 'Iron Sword',
                                'gear_price': 50,
                                'gear_slot': 'Weapon',
                                'gear_stat': 15,
                                'gear_stat_type': 'strength'},
                               {'gear_class': 'common',
                                'gear_id': 3,
                                'gear_name': 'Leather Armor',
                                'gear_price': 30,
                                'gear_slot': 'Armor',
                                'gear_stat': 10,
                                'gear_stat_type': 'defence'},
                               {'gear_class': 'legendary',
                                'gear_id': 4,
                                'gear_name': 'Twig',
                                'gear_price': 100,
                                'gear_slot': 'Weapon',
                                'gear_stat': 90,
                                'gear_stat_type': 'accuracy'},
                               {'gear_class': 'uncommon',
                                'gear_id': 5,
                                'gear_name': 'Steel Armor',
                                'gear_price': 60,
                                'gear_slot': 'Armor',
                                'gear_stat': 20,
                                'gear_stat_type': 'defence'},
                               {'gear_class': 'common',
                                'gear_id': 6,
                                'gear_name': 'Water Pistol',
                                'gear_price': 15,
                                'gear_slot': 'Weapon',
                                'gear_stat': 7,
                                'gear_stat_type': 'speed'},
                               {'gear_class': 'epic',
                                'gear_id': 7,
                                'gear_name': 'Silver Dagger',
                                'gear_price': 80,
                                'gear_slot': 'Weapon',
                                'gear_stat': 60,
                                'gear_stat_type': 'strength'},
                               {'gear_class': 'uncommon',
                                'gear_id': 8,
                                'gear_name': 'Chainmail',
                                'gear_price': 70,
                                'gear_slot': 'Armor',
                                'gear_stat': 20,
                                'gear_stat_type': 'defence'},
                               {'gear_class': 'common',
                                'gear_id': 9,
                                'gear_name': 'Pink Boots',
                                'gear_price': 25,
                                'gear_slot': 'Boots',
                                'gear_stat': 18,
                                'gear_stat_type': 'speed'},
                               {'gear_class': 'common',
                                'gear_id': 10,
                                'gear_name': 'Fork',
                                'gear_price': 5,
                                'gear_slot': 'Weapon',
                                'gear_stat': 3,
                                'gear_stat_type': 'strength'},
                               {'gear_class': 'common',
                                'gear_id': 12,
                                'gear_name': 'mace of sharpness(stick with knife tied to it)',
                                'gear_price': 20,
                                'gear_slot': 'Weapon',
                                'gear_stat': 2,
                                'gear_stat_type': 'strength'},
                               {'gear_class': 'common',
                                'gear_id': 13,
                                'gear_name': 'huge rock',
                                'gear_price': 20,
                                'gear_slot': 'Weapon',
                                'gear_stat': 3,
                                'gear_stat_type': 'strength'},
                               {'gear_class': 'common',
                                'gear_id': 14,
                                'gear_name': 'horny helmet',
                                'gear_price': 20,
                                'gear_slot': 'Head',
                                'gear_stat': 3,
                                'gear_stat_type': 'defence'},
                               {'gear_class': 'epic',
                                'gear_id': 15,
                                'gear_name': 'big spender',
                                'gear_price': 1500,
                                'gear_slot': 'Title',
                                'gear_stat': 3,
                                'gear_stat_type': 'defence'},
                               {'gear_class': 'epic',
                                'gear_id': 16,
                                'gear_name': 'boots of running really fast',
                                'gear_price': 100,
                                'gear_slot': 'Boots',
                                'gear_stat': 15,
                                'gear_stat_type': 'speed'},
                               {'gear_class': 'common',
                                'gear_id': 17,
                                'gear_name': 'rat on a stick(hey its better then nothing)',
                                'gear_price': 1,
                                'gear_slot': 'Weapon',
                                'gear_stat': 1,
                                'gear_stat_type': 'Boots'}]


def test_get_player_loot():
    """ Test the endpoint for retrieving player loot. """

    response = client.get("/shop/loot/1")
    assert response.status_code == 200
    assert response.json() == 'Your current balance is: 0'


def test_get_player_loot_not_found():
    """ Test the endpoint for retrieving player loot. """

    response = client.get("/shop/loot/999")
    assert response.status_code == 404
    assert response.json() == {'detail': 'No player found'}


def test_buy_and_equip_gear():
    """ Test the endpoint for Buy and equip a piece of gear """
# head
    response = client.post("/shop/buy-and-equip/2/1")
    assert response.status_code == 200
    assert response.json() == {
        'message': 'You have bought and equipped Baseball Cap!'}

    # weapon
    response = client.post("/shop/buy-and-equip/2/10")
    assert response.status_code == 200
    assert response.json() == {'message': 'You have bought and equipped Fork!'}

    # armor
    response = client.post("/shop/buy-and-equip/2/5")
    assert response.status_code == 200
    assert response.json() == {
        'message': 'You have bought and equipped Steel Armor!'}

    # boots
    response = client.post("/shop/buy-and-equip/2/9")
    assert response.status_code == 200
    assert response.json() == {
        'message': 'You have bought and equipped Pink Boots!'}

    # title
    response = client.post("/shop/buy-and-equip/2/15")
    assert response.status_code == 200
    assert response.json() == {
        'message': 'You have bought and equipped big spender!'}


def test_buy_and_equip_gear_player_not_found():
    """ Test the endpoint for Buy and equip a piece of gear """

    response = client.post("/shop/buy-and-equip/999/10")
    assert response.status_code == 404
    assert response.json() == {'detail': 'No player found'}


def test_buy_and_equip_gear_gear_not_found():
    """ Test the endpoint for Buy and equip a piece of gear """

    response = client.post("/shop/buy-and-equip/2/999")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Gear not found or not buyable'}


def test_buy_and_equip_gear_no_funds():
    """ Test the endpoint for Buy and equip a piece of gear """

    response = client.post("/shop/buy-and-equip/1/15")
    assert response.status_code == 400
    assert response.json() == {'detail': 'Not enough loot to buy the gear'}
