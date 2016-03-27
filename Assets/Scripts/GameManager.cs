using UnityEngine;
using System.Collections;
using System.Collections.Generic;

public class GameManager : MonoBehaviour {

    public static GameManager Instance;
    public GameObject TilePrefab;
    public GameObject CharacterPrefab;
    public GameObject AIPrefab;

    public int MapSize = 11;
    public int PlayerIndex;

    public List<List<Tile>> map = new List<List<Tile>>();
    public List<Player> players = new List<Player>();

    void Awake()
    {
        Instance = this;
    }

	// Use this for initialization
	void Start ()
    {
        GenerateMap();
        GeneratePlayers();
	}
	
	// Update is called once per frame
	void Update ()
    {
        if (players[PlayerIndex].HP > 0)
        {
            players[PlayerIndex].TurnUpdate(); 
        }
        else
        {
            NextTurn();
        }
	}

    void OnGUI()
    {
        if (players[PlayerIndex].HP > 0)
        {
            players[PlayerIndex].TurnOnGUI();
        }
    }

    public void NextTurn()
    {
        if (PlayerIndex + 1 < players.Count)
        {
            PlayerIndex++;
        }
        else
        {
            PlayerIndex = 0;
        }
    }
    public void moveCurrentPlayer(Tile destinationTile)
    {
        players[PlayerIndex].GridPosition = destinationTile.GridPosition;
        players[PlayerIndex].moveDestination = destinationTile.transform.position + 1.5f * Vector3.up;
    }
    public void attackWithCurrentPlayer(Tile destinationTile)
    {
        Player target = null;
        foreach (Player p in players)
        {
            if (p.GridPosition == destinationTile.GridPosition)
            {
                target = p;
            }
        }
        if (target != null && target.HP > 0 && target != players[PlayerIndex])
        {
            if (players[PlayerIndex].GridPosition.x >= target.GridPosition.x - 1 && players[PlayerIndex].GridPosition.x <= target.GridPosition.x + 1
                && players[PlayerIndex].GridPosition.y >= target.GridPosition.y -1 && players[PlayerIndex].GridPosition.y <= target.GridPosition.y + 1)
            {
                bool critical;
                // kill em
                // D20 to hit vs Defense
                if (RollToHIT(target, out critical))
                {
                    // kill him
                    int dmg = RollDamage(target, critical);
                    Debug.Log("Hit " + target.Name);
                    Debug.Log("The swing causes " + dmg + " raw damage");
                    Debug.Log("The target had " + target.HP + " and now has ");
                    ApplyDamage(target, dmg);
                    if (target.HP > 0)
                    {
                        Debug.Log(target.HP);
                    }
                    else
                    {
                        Debug.Log(0);
                    }
                }
                else
                {
                    // you missed
                    Debug.Log("Missed " + target.Name);
                }
                // HD + base = damage
                // 
                players[PlayerIndex].ActionPoints--;
            }
            else
            {
                Debug.Log(target.Name + " is too far away");
            } 
        }
        else
        {
            Debug.Log("You don't have a target.");
        }
    }
    void GenerateMap()
    {
        map = new List<List<Tile>>(); // set the map to null
        for (int i = 0; i < MapSize; i++)
        {
            List<Tile> row = new List<Tile>();
            for (int j = 0; j < MapSize; j++)
            {
                // create a tile by selecting the tile prefab and  gettings it's Tile component. 
                // we have to cast to game object to use get component
                // set position and rotation...
                Tile tile = ((GameObject)Instantiate(TilePrefab, new Vector3(i - Mathf.Floor(MapSize/2),0, -j + Mathf.Floor(MapSize / 2)), Quaternion.Euler(new Vector3()))).GetComponent<Tile>();
                tile.GridPosition = new Vector2(i, j);
                row.Add(tile);
            }
            map.Add(row);
        }
    }

    void GeneratePlayers()
    {
        UserPlayer player;
        player = ((GameObject)Instantiate(CharacterPrefab, new Vector3(0 - Mathf.Floor(MapSize / 2), 1.45f, 0 + Mathf.Floor(MapSize / 2)), Quaternion.Euler(new Vector3()))).GetComponent<UserPlayer>();
        player.GridPosition = new Vector2(0,0);
        player.Name = "Link";
        players.Add(player);
        Debug.Log(player.ActionPoints);

        player = ((GameObject)Instantiate(CharacterPrefab, new Vector3((MapSize - 1) - Mathf.Floor(MapSize / 2), 1.45f, -(MapSize - 1) + Mathf.Floor(MapSize / 2)), Quaternion.Euler(new Vector3()))).GetComponent<UserPlayer>();
        player.GridPosition = new Vector2(14,14);
        player.Name = "Mario";
        players.Add(player);
        Debug.Log(player.ActionPoints);

        player = ((GameObject)Instantiate(CharacterPrefab, new Vector3(4 - Mathf.Floor(MapSize / 2), 1.45f, -4 + Mathf.Floor(MapSize / 2)), Quaternion.Euler(new Vector3()))).GetComponent<UserPlayer>();
        player.GridPosition = new Vector2(4,4);
        player.Name = "Marth";
        players.Add(player);
        Debug.Log(player.ActionPoints);

        //AIPlayer aiplayer = ((GameObject)Instantiate(AIPrefab, new Vector3(6 - Mathf.Floor(MapSize / 2), 1.45f, -4 + Mathf.Floor(MapSize / 2)), Quaternion.Euler(new Vector3()))).GetComponent<AIPlayer>();
        //players.Add(aiplayer);
        foreach (Player p in players)
        {
            Debug.Log(p.GridPosition);
        }
    }

    // COMBAT information. To be moved to separate class
    public bool RollToHIT(Player target, out bool critical)
    {
        int die = Random.Range(1, 20);
        bool hit = (die + players[PlayerIndex].hitChance > target.defenseChance);
        if (die == 20)
        {
            hit = true;
            critical = true;
        }
        else if (hit)
        {
            hit = true;
            critical = false;
        }
        else
        { 
            hit = false;
            critical = false;
        }
        return hit;
    }

    public int RollDamage(Player target, bool critical)
    {
        int damage = Random.Range(0,players[PlayerIndex].HitDie) + players[PlayerIndex].damageBase;
        if (critical)
        {
            damage = damage * 2;
        }
        return damage;
    }

    public void ApplyDamage(Player target, int DamageDone)
    {
        target.HP -= (DamageDone-target.DamageReduction); // subtract DR from damage than modify target HP
    }
}
