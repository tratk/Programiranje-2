import java.awt.geom.Point2D;
import java.util.ArrayList;
import java.util.List;
import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.FontMetrics;
import javax.swing.JButton;
import javax.swing.JComboBox;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.Timer;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;

public class Snake_game extends JFrame {
	private Snake snake;
	private Food food;
	private boolean playing; //ali se igra izvaja
	private List<Point2D> wall;
	
	
	public Snake_game() {
		super();
		this.snake = new Snake(3, 30);
		this.food = new Food(0, 0, 30);
		this.playing = false;
		this.wall = new ArrayList<Point2D>();
		
		setTitle("Snake");
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		getRootPane().putClientProperty("apple.awt.brushMetalLook", true);
		setMinimumSize(new Dimension(981, 682));
		setLayout(new BorderLayout());
		setResizable(false);
		
		
		
		
		Timer timer = new Timer(300 - (int)((snake.getLength() -3)*260/1440), new ActionListener() {
			//na zacetku premakne vsakih 300ms, pri maksimalni dolzini kace pa vsakih 40ms
			//1440 - stevilo vseh tock na polju pri velikosti kace 20
	        @Override
	        public void actionPerformed(ActionEvent e) {
	            if(snake.getAlive()) {
	            	if ((int)(snake.getNext().getX()) == food.getX() && (int)(snake.getNext().getY()) == food.getY()) { //kaca poje hrano
	            		snake.feed(); //povecam kaco
	            		snake.move(wall); //premaknem kaco
	            		food.move(snake.getPositions(), wall); //premaknem hrano
	            	}
	            	else snake.move(wall); //samo premaknem
	            	if (snake.getAlive()) repaint();
	            } else {
	                ((Timer)e.getSource()).stop();
	                playing = false; //kaca ni vec ziva, konec igre
	                repaint();
	            }
	        }
	    });
		
		JPanel panel = new JPanel();
		panel.setFocusable(true);
		panel.setBackground(Color.BLACK);
		add(panel, BorderLayout.CENTER);
		
		panel.addKeyListener(new KeyListener() {

			@Override
			public void keyTyped(KeyEvent e) {
				// TODO Auto-generated method stub
			}

			@Override
			public void keyPressed(KeyEvent e) { //nastavim smer
				if(e.getKeyCode() == KeyEvent.VK_UP) {
					if (snake.getDirection() != 3) {
						snake.setDirection(1);
					}
				}
				else if(e.getKeyCode() == KeyEvent.VK_DOWN) {
					if (snake.getDirection() != 1) {
						snake.setDirection(3);
					}
				}
				else if(e.getKeyCode() == KeyEvent.VK_RIGHT) {
					if (snake.getDirection() != 2) {
						snake.setDirection(0);
					}
				}
				else if(e.getKeyCode() == KeyEvent.VK_LEFT) {
					if (snake.getDirection() != 0) {
						snake.setDirection(2);
					}
				}
			}

			@Override
			public void keyReleased(KeyEvent e) {
				// TODO Auto-generated method stub
			}
			
		});
		
		JLabel dif = new JLabel("Difficulty:"); //dodam tezavnosti
		dif.setForeground(Color.white);
		dif.setFocusable(false);
		panel.add(dif);
		JComboBox<String> difficulty = new JComboBox<String>(new String[] { "Easy", "Medium", "Hard"});
		difficulty.setFocusable(false);
		panel.add(difficulty);
		
		JButton button = new JButton("Start");
		button.setFocusable(false);
		button.addActionListener(new ActionListener() {

			@Override
			public void actionPerformed(ActionEvent e) { //igra se zacne
				snake.setLength(3);
				if ((String) difficulty.getSelectedItem() == "Easy") { //kaca je vecja, polje ima manj tock
					wall = new ArrayList<Point2D>();
					snake.setSize(30);
					food.setSize(30);
					food.move(snake.getPositions(), wall); //premaknem hrano na random pozicijo
				}
				else if ((String) difficulty.getSelectedItem() == "Medium") { //kaca je manjsa, polje ima vec tock
					wall = new ArrayList<Point2D>();
					snake.setSize(20);
					food.setSize(20);
					food.move(snake.getPositions(), wall); //premaknem hrano na random pozicijo
				}
				else { // kaca enaka kot pri medium, dodam se zid na polje
					wall = new ArrayList<Point2D>();
					snake.setSize(20);
					food.setSize(20);
					//generacija zidu
					for(int i = 0; i < 10; ++i) {
						wall.add(new Point2D.Double(7 + i, 7));
						wall.add(new Point2D.Double(32 + i, 7));
						wall.add(new Point2D.Double(7 + i, 22));
						wall.add(new Point2D.Double(32 + i, 22));
					}
					for(int i = 0; i < 16; ++i) {
						wall.add(new Point2D.Double(7, 7 + i));
						wall.add(new Point2D.Double(41, 7 + i));
					}
					food.move(snake.getPositions(), wall);
				}
				
				playing = true; //zacnem igro
				snake.setAlive(true);
				snake.setDirection(0); //nastavim zacetno smer v desno
				repaint();
				timer.start();
				}
			
			
		});
		panel.add(button);

	}
	
	
	
	@Override
    public void paint(Graphics g) {
		super.paint(g);
		Graphics2D	graphics = (Graphics2D)g;
		if(playing) { //igra poteka
			graphics.setColor(Color.GREEN); //narisem rob igralnega polja
			graphics.drawLine(9, 69, 971, 69);
			graphics.drawLine(9, 69, 9, 671);
			graphics.drawLine(9, 671, 971, 671);
			graphics.drawLine(971, 671, 971, 69);
			
			graphics.setFont(new Font("Montserrat", Font.BOLD, 20)); //dodam sledilec rezultata v desni zgornji kot
			graphics.drawString("Score: " + Integer.toString(snake.getLength() - 3), 20, 57);
			
			
			graphics.setColor(Color.RED); //narisem hrano
			graphics.fillRect((int)(food.getX() * snake.getSize() + 10), (int)(food.getY() * snake.getSize() + 70), snake.getSize(), snake.getSize());
			graphics.setColor(Color.BLACK);
			graphics.drawRect((int)(food.getX() * snake.getSize() + 10), (int)(food.getY() * snake.getSize() + 70), snake.getSize(), snake.getSize());
			
			graphics.setColor(Color.BLUE);
			for(int i = 0; i < snake.getLength(); ++i) { //narisem kaco
				graphics.fillRect((int)(snake.getPositions().get(i).getX() * snake.getSize() + 10), (int)(snake.getPositions().get(i).getY() * snake.getSize() + 70), snake.getSize(), snake.getSize());
				graphics.setColor(Color.BLACK);
				graphics.drawRect((int)(snake.getPositions().get(i).getX() * snake.getSize() + 10), (int)(snake.getPositions().get(i).getY() * snake.getSize() + 70), snake.getSize(), snake.getSize());
				graphics.setColor(Color.GREEN);
			}
			graphics.setColor(Color.YELLOW);
			for(int i = 0; i < wall.size(); ++i) { //narisem zid
				graphics.fillRect((int)(wall.get(i).getX() * 20 + 10), (int)(wall.get(i).getY() * 20 + 70), 20, 20);
			}
		}
		else if (!snake.getAlive()) { //kaca je mrtva, narisem zaslon ob koncu igre
			graphics.setColor(Color.GREEN);
			graphics.setFont(new Font("Montserrat", Font.BOLD, 50));
			graphics.drawString("GAME OVER", 340, 360);
			
			graphics.setFont(new Font("Montserrat", Font.BOLD, 20));
			graphics.drawString("Score: " + Integer.toString(snake.getLength() - 3), 450, 400);
		}
		else { //zacetni zaslon
			graphics.setColor(Color.GREEN);
			graphics.setFont(new Font("Montserrat", Font.BOLD, 250));
			graphics.drawString("SNAKE", 45, 460);
		}
	}
	
	public static void main(String[] args) {
		new Snake_game().setVisible(true);
	}

}



class Snake {
	private List<Point2D> positions;
	private int direction;
	private int length;
	private boolean alive;
	private int mx;
	private int my;
	private int size;
	
	public Snake(int length, int size) {
		this.direction = 0;
		this.length = length;
		this.mx = (int)(960 / size); //najvecji x in y, velikost polja / velikost kace
		this.my = (int)(600 / size);
		this.size = size;
		this.alive = true;
		this.positions = new ArrayList<Point2D>();
		for (int i = 0; i < length; ++i) { //zacetne pozicije na sredini polja
			positions.add(new Point2D.Double((mx / 2) - i, my / 2));
		}
	}
	
	public List<Point2D> getPositions(){
		return positions;
	}
	
	
	public int getDirection() {
		return direction;
	}
	
	public int getLength() {
		return length;
	}
	
	public void setLength(int l) {
		length = l;
	}
	
	public void setDirection(int s) {
		direction = s;
	}
	
	public int getSize() {
		return size;
	}
	
	public void setSize(int s) {
		size = s;
		//moram se na novo definirati maksimalne koordinate in postaviti kaco na sredino novega polja
		mx = (int)(960 / size);
		my = (int)(600 / size);
		positions = new ArrayList<Point2D>();
		for (int i = 0; i < length; ++i) {
			positions.add(new Point2D.Double((mx / 2) - i, my / 2));
		}
	}
	
	public boolean getAlive() {
		return alive;
	}
	
	public void setAlive(boolean a) {
		alive = a;
	}
	
	public Point2D getNext() { //naslednja pozicija glave kace
		return new Point2D.Double(positions.get(0).getX() + (int)(Math.cos(direction*Math.PI/2)), positions.get(0).getY() - (int)(Math.sin(direction*Math.PI/2)));
	// smer ima vrednosti 0, 1, 2, ali 3, torej 0*90 stopinj je v desno in podobno za ostale
	}
	
	public void move(List<Point2D> wall) { //premakne kaco za eno poje naprej v smeri gibanja
		Point2D next = new Point2D.Double(positions.get(0).getX() + (int)(Math.cos(direction*Math.PI/2)), positions.get(0).getY() - (int)(Math.sin(direction*Math.PI/2)));
		if (next.getX() >= mx || next.getY() >= my || next.getY() < 0 || next.getX() < 0) { //kaca  bi sla izven polja
			alive = false;
		}
		else {
			for(int i = 0; i < wall.size(); ++i) { //kaca bi se zabila v zid
				if(wall.indexOf(next) != -1) {
					alive = false;
				}
			}
			for (int i = length - 1; i > 0; --i) {
				positions.set(i, positions.get(i-1)); // premaknem vsako tocko naprej
				if (positions.get(i).getX() == next.getX() && positions.get(i).getY() == next.getY()) { //preverim, da se kaca ne zabije sama vase
					alive = false;
				}
			}
			positions.set(0, next); //prva tocka za ena naprej
		}
	}
	
	public void feed() { //kaca poje hrano, dodam eno enoto na konec kace
		Point2D t1 = positions.get(positions.size() - 1);
		Point2D t2 = positions.get(positions.size() - 2);
		positions.add(new Point2D.Double(2 * t1.getX() - t2.getX(), 2 * t1.getY() - t2.getY()));
		length += 1;
	}
}

class Food{
	private int x;
	private int y;
	private int size;
	
	public Food(int x, int y, int size) {
		this.x = x;
		this.y = y;
		this.size = size;
	}
	
	
	public int getX() {
		return x;
	}
	
	public int getY() {
		return y;
	}
	
	public void setSize(int s) {
		size = s;
	}
	
	public void move(List<Point2D> positions, List<Point2D> wall) { //premaknem hrano na prazno polje
		List<Point2D> empty = new ArrayList<Point2D>();
		for(int i = 0; i < (int)(960 / size); ++i) { //gre po vseh tockah na polju in si shrani tiste, ki niso zasedene s cim drugim
			for(int j = 0; j <(int)(600 / size); ++j) {
				if(positions.indexOf(new Point2D.Double(i, j)) == -1 && wall.indexOf(new Point2D.Double(i, j)) == -1) {
					empty.add(new Point2D.Double(i, j));
				}
			}
		}
		
		Point2D t = empty.get((int)(Math.random() * empty.size())); //izbere random tocko izmed praznih
		x = (int) t.getX();
		y = (int) t.getY();
	}
}