using UnityEngine;
using System.Collections;

public class Player : MonoBehaviour {

    public Vector3 moveDestination;
    public Vector2 GridPosition = Vector3.zero;
    public bool moving = false;
    public bool attacking = false;
    
    // these are static for now and will be converted when the classes for the RPG elements are added
    public int HP = 25;
    public int hitChance = 2; // base attack bonus!
    public int defenseChance = 15; // AC
    public int damageBase = 5;
    public int HitDie = 6;
    public int DamageReduction = 2; // DR valule (armour and shields and stuff)
    public int ActionPoints;
    public int AttackRange;
    public int MovementRange;
    public string Name;

    void Awake()
    {
        ActionPoints = 2;
        AttackRange = 1;
        MovementRange = 4;
        moveDestination = transform.position;
    }

	// Use this for initialization
	void Start () {
	}
	
	// Update is called once per frame
	public virtual void Update () {
        if (HP <= 0)
        {
            transform.rotation = Quaternion.Euler(new Vector3(transform.rotation.eulerAngles.x + 90, transform.rotation.eulerAngles.x, transform.rotation.eulerAngles.x));
            rend.material.color = Color.red;
        }
    }
    public virtual void TurnUpdate()
    {
        if (ActionPoints <= 0)
        {
            ActionPoints = 2;
            moving = false;
            attacking = false;
            GameManager.Instance.NextTurn();
        }
    }
    public virtual void TurnOnGUI()
    {

    }
    void OnGUI()
    {
	    // display HP
	    Vector3 location = Camera.main.WorldToScreenPoint(transform.position) + Vector3.up * 75;
        GUI.Label(new Rect(location.x, Screen.height - location.y,30,20), HP.ToString());
    }
}
