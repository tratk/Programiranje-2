import java.awt.geom.Point2D;
import java.util.ArrayList;
import java.util.List;

public class Igra {
	
	public static void main(String[] args) {
		Kaca kaca = new Kaca(3, 10, 10);
		kaca.premakni();
		System.out.println(kaca.getPozicije());
	}
	
	
}

class Kaca {
	private List<Point2D> pozicije = new ArrayList<Point2D>();
	private int smer;
	private int dolzina;
	private boolean ziva;
	private int mx;
	private int my;
	
	public Kaca(int dolzina, int mx, int my) {
		this.smer = 0;
		this.dolzina = dolzina;
		this.mx = mx;
		this.my = my;
		this.ziva = true;
		this.pozicije = new ArrayList<Point2D>();
		for (int i = 0; i < dolzina; ++i) {
			pozicije.add(new Point2D.Double(-i, 0));
		}
	}
	
	public List<Point2D> getPozicije(){
		return pozicije;
	}
	
	
	public int getSmer() {
		return smer;
	}
	
	public void setSmer(int s) {
		smer = s;
	}
	
	public boolean getZiva() {
		return ziva;
	}
	
	public void premakni() {
		Point2D naslednja = new Point2D.Double(pozicije.get(0).getX() + (int)(Math.cos(smer*Math.PI/2)), pozicije.get(0).getY() + (int)(Math.sin(smer*Math.PI/2)));
		if (Math.abs(naslednja.getX()) > mx || Math.abs(naslednja.getY()) > my) {
			ziva = false;
		}
		for (int i = dolzina - 1; i > 0; --i) {
			pozicije.set(i, pozicije.get(i-1));
			if (pozicije.get(i).getX() == naslednja.getX() && pozicije.get(i).getY() == naslednja.getY()) {
				ziva = false;
			}
		}
		pozicije.set(0, naslednja);
	}
}

class Jabolko{
	private int x;
	private int y;
	
	public Jabolko(int x, int y) {
		this.x = x;
		this.y = y;
	}
	
	public int getX() {
		return x;
	}
	
	public int getY() {
		return y;
	}
	
	public void narediNovo(int mx, int my, List<Integer> pozicijeX, List<Integer> pozicijeY) {
		
	}
}