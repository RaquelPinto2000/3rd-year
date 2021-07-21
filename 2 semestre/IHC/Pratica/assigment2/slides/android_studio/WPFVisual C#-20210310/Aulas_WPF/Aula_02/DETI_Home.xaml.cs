using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace Aula_02
{
    /// <summary>
    /// Interaction logic for DETI_Home.xaml
    /// </summary>
    public partial class DETI_Home : Page
    {
        public DETI_Home()
        {
            InitializeComponent();
        }

        private void Navigate()
        {
            if ((ListBoxItem)cursosListBox.SelectedValue == null)
                MessageBox.Show("Selecione um curso", "Erro", MessageBoxButton.OK);
            else
            {
                DETI_Cursos cursosPage = new DETI_Cursos();
                cursosPage.nomeCurso.Content = ((ListBoxItem)cursosListBox.SelectedValue).Content.ToString();
                this.NavigationService.Navigate(cursosPage);
            }
        }

        private void Button_Click(object sender, RoutedEventArgs e)
        {
            Navigate();
        }

        private void cursosListBox_MouseDoubleClick(object sender, MouseButtonEventArgs e)
        {
            Navigate();
        }
    }
}
